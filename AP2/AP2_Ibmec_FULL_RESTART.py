"""
AP2_Ibmec_FULL_RESTART.py
--------------------------
Reconstrói TODA a cena do zero, em um arquivo Blender vazio, e já entrega
com a animação completa. Resolve os bugs anteriores criando cada letra de
"Ibmec" como um OBJETO INDEPENDENTE desde a criação (em vez de separar
depois um texto único) — assim não há ambiguidade de qual pedaço é qual
letra.

COMO USAR:
1. Abra o Blender 4.5 LTS e crie um arquivo NOVO (File > New > General).
2. Vá em Scripting, cole este código em um novo Text.
3. Clique em Run Script.
4. Salve como AP2_NomeSobrenome.blend.
5. Revise no Timeline / Graph Editor, ajuste se quiser, renderize com
   Ctrl+F12 (ou Render > Render Animation).

O QUE É CONSTRUÍDO:
- Coleção "AP1_Ibmec_Conceito" com:
    Letra_I, Letra_b, Letra_m, Letra_e, Letra_c  (texto convertido em
    malha, cada letra seu próprio objeto, material da marca)
    Obj_Luminaria, Obj_Orbe, Obj_Garra            (os 3 objetos autorais)
    Camera_Principal
- Coleção "AC04_Luzes" com Light_Principal (Area) e Light_Preenchimento (Sun)

A NARRATIVA ANIMADA (1–360, 24fps):
1. A luminária cai de cima e ESMAGA a letra "I" ao aterrissar (squash),
   exatamente na posição do "I" — frames 1–70, impacto no frame 50.
2. A letra "I" fica "invisível" (escala ~0) até o instante do impacto,
   quando estampa no lugar.
3. A garra entrega as letras b, m, e, c UMA POR UMA, nessa ordem, cada
   uma chegando voando e sendo posicionada pela garra — frames 90–320.
4. O orbe sobe, se acomoda em cima da luminária e passa a BRILHAR como
   um farol (emissão + luz puntual) — frames 330–360.
5. Câmera com leve aproximação ao longo de toda a peça.
6. Render configurado: Eevee, 1920x1080, 24fps, frames 1-360, saída
   .mp4 (H.264).
"""

import bpy
import math
from mathutils import Vector


# ===========================================================================
# UTILIDADES
# ===========================================================================

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block_list in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
                       bpy.data.lights, bpy.data.cameras, bpy.data.actions):
        for block in list(block_list):
            if block.users == 0:
                block_list.remove(block)


def get_or_create_collection(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def move_to_collection(obj, collection):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)


def select_only(obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)


def keyframe_lrs(obj, frame, loc=True, rot=True, scale=True):
    if loc:
        obj.keyframe_insert(data_path="location", frame=frame)
    if rot:
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
    if scale:
        obj.keyframe_insert(data_path="scale", frame=frame)


def world_bbox_center(obj):
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    center = Vector((0.0, 0.0, 0.0))
    for c in corners:
        center += c
    return center / 8.0


def new_simple_material(name, color, metallic, roughness):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat, bsdf


# ===========================================================================
# PALAVRA "Ibmec" — cada letra é seu próprio objeto desde a criação
# ===========================================================================

LETTERS = ["I", "b", "m", "e", "c"]
LETTER_NAMES = ["Letra_I", "Letra_b", "Letra_m", "Letra_e", "Letra_c"]


def create_word_letters(collection, mat):
    size = 1.6
    extrude = 0.08
    bevel_depth = 0.015
    bevel_resolution = 3
    gap = 0.35

    objs = []
    cursor_x = 0.0

    for char, name in zip(LETTERS, LETTER_NAMES):
        curve_data = bpy.data.curves.new(name=f"{name}_Curve", type='FONT')
        curve_data.body = char
        curve_data.size = size
        curve_data.extrude = extrude
        curve_data.bevel_depth = bevel_depth
        curve_data.bevel_resolution = bevel_resolution
        curve_data.align_x = 'LEFT'
        curve_data.align_y = 'BOTTOM'

        obj = bpy.data.objects.new(name, curve_data)
        bpy.context.scene.collection.objects.link(obj)
        obj.location = (cursor_x, 0.0, 0.0)

        select_only(obj)
        bpy.ops.object.convert(target='MESH')

        width = obj.dimensions.x if obj.dimensions.x > 0 else size * 0.5
        cursor_x += width + gap

        obj.data.materials.clear()
        obj.data.materials.append(mat)

        objs.append(obj)

    total_width = cursor_x - gap
    shift = -total_width / 2.0
    for obj in objs:
        obj.location.x += shift
        # Texto nasce "deitado" no plano XY (lido de cima); gira +90° em X
        # para ficar de pé, com a face de leitura voltada para a câmera
        # (que olha ao longo do eixo Y).
        obj.rotation_euler.x = math.radians(90)
        select_only(obj)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        # Corrige qualquer resíduo de altura: força a base da letra a
        # encostar exatamente em z = 0 (mesmo nível do chão/luminária),
        # recalculando pela caixa delimitadora real em vez de confiar no
        # alinhamento 'BOTTOM' do texto.
        bpy.context.view_layer.update()
        corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        min_z = min(c.z for c in corners)
        obj.location.z -= min_z

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        move_to_collection(obj, collection)

    return {name: obj for name, obj in zip(LETTER_NAMES, objs)}


# ===========================================================================
# OBJETO AUTORAL 1: Luminária articulada
# ===========================================================================

def create_lamp(collection, location):
    """
    Luminária em formato RETO (poste vertical + base + cabeça esférica),
    para que, ao pousar, ela funcione visualmente como o "novo I" — com
    o Obj_Orbe pousando em cima da cabeça como o ponto.
    """
    lx, ly, lz = location
    parts = []

    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=0.12, location=(lx, ly, lz + 0.06))
    base = bpy.context.object
    base.name = "Lamp_Base"
    parts.append(base)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=1.3, location=(lx, ly, lz + 0.77))
    stem = bpy.context.object
    stem.name = "Lamp_Stem"
    parts.append(stem)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.16, location=(lx, ly, lz + 1.58))
    head = bpy.context.object
    head.name = "Lamp_Head"
    mod = head.modifiers.new(name="Subsurf", type='SUBSURF')
    mod.levels = 2
    mod.render_levels = 2
    parts.append(head)

    select_only(base)
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()

    lamp_obj = bpy.context.object
    lamp_obj.name = "Obj_Luminaria"

    # Origem no ponto de contato com o chão (base), para que reduzir a
    # escala encolha a luminária "de cima para baixo" sem levantar a base.
    bpy.context.scene.cursor.location = (lx, ly, lz)
    select_only(lamp_obj)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

    # Reduz a altura total para não ficar muito mais alta que as letras.
    lamp_obj.scale = (0.65, 0.65, 0.65)

    # Correção final: garante que a base realmente encosta em z = lz,
    # recalculando pela caixa delimitadora real (evita qualquer resíduo
    # de deslocamento vindo das etapas anteriores).
    bpy.context.view_layer.update()
    corners = [lamp_obj.matrix_world @ Vector(c) for c in lamp_obj.bound_box]
    min_z = min(c.z for c in corners)
    lamp_obj.location.z += (lz - min_z)

    move_to_collection(lamp_obj, collection)
    return lamp_obj


# ===========================================================================
# OBJETO AUTORAL 2: Orbe estilizado
# ===========================================================================

def create_orb(collection, location):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.16, location=location)
    orb = bpy.context.object
    orb.name = "Orb_Core"

    bpy.context.view_layer.objects.active = orb
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.inset(thickness=0.012, depth=0.0)
    bpy.ops.object.mode_set(mode='OBJECT')

    rings = [orb]
    for i, rot in enumerate([(0, 0, 0), (math.radians(60), 0, 0), (0, math.radians(60), 0)]):
        bpy.ops.mesh.primitive_torus_add(location=location, rotation=rot,
                                          major_radius=0.22, minor_radius=0.01,
                                          major_segments=24, minor_segments=8)
        ring = bpy.context.object
        rings.append(ring)

    select_only(orb)
    for r in rings:
        r.select_set(True)
    bpy.context.view_layer.objects.active = orb
    bpy.ops.object.join()

    orb_obj = bpy.context.object
    orb_obj.name = "Obj_Orbe"
    move_to_collection(orb_obj, collection)
    return orb_obj


# ===========================================================================
# OBJETO AUTORAL 3: Garra mecânica
# ===========================================================================

FINGER_OFFSETS = [(-0.17, 0.0), (0.0, 0.19), (0.17, 0.0)]
# Rotação (rad) de cada dedo quando ABERTO; fechado = (0,0,0) (reto, agarrando).
FINGER_OPEN_ROT = [
    (0.0, math.radians(60), 0.0),
    (math.radians(60), 0.0, 0.0),
    (0.0, math.radians(-60), 0.0),
]
FINGER_CLOSED_ROT = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]


def create_claw(collection, location):
    """
    Garra com o corpo (hub) e os 3 dedos como objetos SEPARADOS, filhos do
    hub, para poder animar cada dedo abrindo/fechando (agarrando) de
    verdade. Desenho mais elaborado: corpo cônico + pulso + anel
    decorativo + dedos afunilados com uma junta ("nó") no meio.
    Retorna (hub, lista_de_3_dedos).
    """
    lx, ly, lz = location

    # Braço: bem comprido, para sair do quadro por cima em vez de parecer
    # um toco curto flutuando — dá a sensação de estar preso a algo fora
    # da câmera.
    ARM_LENGTH = 5.0
    bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=ARM_LENGTH,
                                         location=(lx, ly, lz + 0.28 + ARM_LENGTH / 2.0))
    wrist = bpy.context.object
    wrist.name = "Claw_Braco"

    # Corpo cônico (mais elegante que um cilindro reto).
    bpy.ops.mesh.primitive_cone_add(radius1=0.17, radius2=0.11, depth=0.28,
                                     location=(lx, ly, lz + 0.14))
    body = bpy.context.object
    body.name = "Claw_Corpo"

    # Anel decorativo na base do corpo, onde os dedos se encaixam.
    bpy.ops.mesh.primitive_torus_add(location=(lx, ly, lz), major_radius=0.17, minor_radius=0.014,
                                      major_segments=28, minor_segments=8)
    collar = bpy.context.object
    collar.name = "Claw_Anel"

    select_only(wrist)
    body.select_set(True)
    collar.select_set(True)
    bpy.context.view_layer.objects.active = wrist
    bpy.ops.object.join()
    hub = bpy.context.object
    hub.name = "Obj_Garra"

    # O join() herda a origem do objeto ativo (o braço comprido), que
    # ficaria no meio do braço. Recoloca a origem no ponto de "pega"
    # (base do corpo, onde os dedos se encaixam) para que claw.location
    # volte a representar o ponto onde a garra efetivamente segura algo.
    bpy.context.scene.cursor.location = (lx, ly, lz)
    select_only(hub)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)

    bevel_mod = hub.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.width = 0.012
    bevel_mod.segments = 2

    move_to_collection(hub, collection)

    attach_z = lz  # base do corpo cônico, onde os dedos se encaixam
    finger_length = 0.5

    fingers = []
    for i, (dx, dy) in enumerate(FINGER_OFFSETS):
        center_z = attach_z - finger_length / 2.0
        bpy.ops.mesh.primitive_cone_add(radius1=0.045, radius2=0.016, depth=finger_length,
                                         location=(lx + dx, ly + dy, center_z))
        finger = bpy.context.object
        finger.name = f"Obj_Garra_Dedo{i + 1}"

        # Junta/nó decorativo a cerca de 1/3 do dedo (visual de dobradiça).
        knuckle_z = attach_z - finger_length * 0.32
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(lx + dx, ly + dy, knuckle_z))
        knuckle = bpy.context.object

        select_only(finger)
        knuckle.select_set(True)
        bpy.context.view_layer.objects.active = finger
        bpy.ops.object.join()
        finger = bpy.context.object

        bpy.context.view_layer.objects.active = finger
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bevel(offset=0.006, segments=2, affect='EDGES')
        bpy.ops.object.mode_set(mode='OBJECT')

        # Origem no ponto de encaixe (topo do dedo) para ele girar como
        # uma dobradiça presa ao hub, em vez de girar no próprio meio.
        bpy.context.scene.cursor.location = (lx + dx, ly + dy, attach_z)
        select_only(finger)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        select_only(finger)
        hub.select_set(True)
        bpy.context.view_layer.objects.active = hub
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        move_to_collection(finger, collection)
        fingers.append(finger)

    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
    return hub, fingers


# ===========================================================================
# CÂMERA e LUZES
# ===========================================================================

def create_camera(collection, target_center):
    cam_data = bpy.data.cameras.new("Camera_Principal_Data")
    cam_data.lens = 50
    cam_obj = bpy.data.objects.new("Camera_Principal", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    move_to_collection(cam_obj, collection)
    cam_obj.location = (target_center.x, target_center.y - 8.0, target_center.z + 1.0)
    cam_obj.rotation_euler = (math.radians(90), 0.0, 0.0)
    bpy.context.scene.camera = cam_obj
    return cam_obj


def create_backdrop(collection, word_center):
    """Chão + parede de fundo com gradiente, para dar profundidade/cenário."""
    # Chão
    bpy.ops.mesh.primitive_plane_add(size=20, location=(word_center.x, word_center.y, -0.01))
    ground = bpy.context.object
    ground.name = "BG_Chao"
    mat_ground, _ = new_simple_material("MAT_Chao", (0.07, 0.07, 0.08, 1.0), 0.0, 0.85)
    ground.data.materials.append(mat_ground)
    move_to_collection(ground, collection)

    # Parede de fundo, mais atrás (+Y), de frente para a câmera, com
    # gradiente vertical (mais escuro embaixo, mais claro em cima).
    bpy.ops.mesh.primitive_plane_add(size=20, location=(word_center.x, word_center.y + 6.0, 5.0))
    wall = bpy.context.object
    wall.name = "BG_Parede"
    wall.rotation_euler = (math.radians(90), 0.0, 0.0)

    mat_wall = bpy.data.materials.new("MAT_Fundo_Gradiente")
    mat_wall.use_nodes = True
    nt = mat_wall.node_tree
    bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    tex_coord = nt.nodes.new('ShaderNodeTexCoord')
    sep_xyz = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.02, 0.02, 0.035, 1.0)
    ramp.color_ramp.elements[1].color = (0.14, 0.15, 0.20, 1.0)
    nt.links.new(tex_coord.outputs['Generated'], sep_xyz.inputs['Vector'])
    nt.links.new(sep_xyz.outputs['Z'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.9
    wall.data.materials.append(mat_wall)
    move_to_collection(wall, collection)

    return ground, wall


def enable_camera_dof(cam, focus_point, collection):
    """Profundidade de campo: fundo levemente desfocado para dar sensação
    de profundidade. O foco fica num Empty que pode ser movido depois."""
    empty = bpy.data.objects.new("Foco_Palavra", None)
    bpy.context.scene.collection.objects.link(empty)
    empty.location = focus_point
    move_to_collection(empty, collection)

    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = empty
    cam.data.dof.aperture_fstop = 2.0
    return empty


def create_lights(collection):
    key_data = bpy.data.lights.new(name="Light_Key_Data", type='AREA')
    key_data.energy = 400.0
    key_data.size = 1.5
    key_data.color = (1.0, 0.98, 0.92)
    key_obj = bpy.data.objects.new("Light_Principal", key_data)
    bpy.context.scene.collection.objects.link(key_obj)
    move_to_collection(key_obj, collection)
    key_obj.location = (-1.5, -4.0, 3.5)
    key_obj.rotation_euler = (0.9, 0.0, -0.4)

    fill_data = bpy.data.lights.new(name="Light_Fill_Data", type='SUN')
    fill_data.energy = 0.6
    fill_data.color = (0.85, 0.9, 1.0)
    fill_obj = bpy.data.objects.new("Light_Preenchimento", fill_data)
    bpy.context.scene.collection.objects.link(fill_obj)
    move_to_collection(fill_obj, collection)
    fill_obj.rotation_euler = (1.0, 0.0, 2.3)

    return key_obj, fill_obj


# ===========================================================================
# ANIMAÇÃO
# ===========================================================================

def animate_lamp_squash(lamp, fall_from, impact_frame, rebound_frame):
    final_loc = lamp.location.copy()
    final_rot = lamp.rotation_euler.copy()
    final_scale = lamp.scale.copy()

    lamp.location = final_loc + Vector(fall_from)
    keyframe_lrs(lamp, 1)

    squashed = Vector((final_scale.x * 1.25, final_scale.y * 1.25, final_scale.z * 0.55))
    lamp.location = final_loc
    lamp.scale = squashed
    keyframe_lrs(lamp, impact_frame)

    lamp.scale = Vector((final_scale.x * 0.95, final_scale.y * 0.95, final_scale.z * 1.08))
    keyframe_lrs(lamp, impact_frame + 6)

    lamp.scale = final_scale
    keyframe_lrs(lamp, rebound_frame)
    keyframe_lrs(lamp, 360)


def animate_letter_crushed(letter, impact_frame):
    """A letra existe normalmente, é esmagada no impacto e então some."""
    final_scale = letter.scale.copy()

    letter.scale = final_scale
    keyframe_lrs(letter, 1, loc=False, rot=False)
    keyframe_lrs(letter, impact_frame - 1, loc=False, rot=False)

    # Achata na hora do impacto (esmagada)
    squashed = Vector((final_scale.x * 1.3, final_scale.y * 1.3, final_scale.z * 0.25))
    letter.scale = squashed
    keyframe_lrs(letter, impact_frame, loc=False, rot=False)

    # Some logo em seguida
    vanish_frame = impact_frame + 14
    letter.scale = Vector((0.001, 0.001, 0.001))
    keyframe_lrs(letter, vanish_frame, loc=False, rot=False)
    keyframe_lrs(letter, 360, loc=False, rot=False)


def set_finger_pose(fingers, rotations, frame):
    for finger, rot in zip(fingers, rotations):
        finger.rotation_euler = Vector(rot)
        finger.keyframe_insert(data_path="rotation_euler", frame=frame)


def animate_claw_delivering_letters(claw, fingers, letters_with_offsets, approach_height=0.6):
    first_letter, first_offset, first_pick, _, _ = letters_with_offsets[0]
    first_center = world_bbox_center(first_letter)
    claw.location = first_center + first_offset + Vector((0, 0, approach_height))
    keyframe_lrs(claw, 1, scale=False)
    set_finger_pose(fingers, FINGER_OPEN_ROT, 1)

    for letter_obj, offset, pick_frame, drop_frame, retreat_frame in letters_with_offsets:
        final_center = world_bbox_center(letter_obj)
        final_loc = letter_obj.location.copy()
        entry_loc = final_loc + offset

        letter_obj.location = entry_loc
        keyframe_lrs(letter_obj, pick_frame, rot=False, scale=False)

        letter_obj.location = final_loc
        keyframe_lrs(letter_obj, drop_frame, rot=False, scale=False)
        keyframe_lrs(letter_obj, 360, rot=False, scale=False)

        pick_point = final_center + offset + Vector((0, 0, approach_height))
        claw.location = pick_point
        keyframe_lrs(claw, pick_frame, scale=False)

        # Dedos fecham (agarram) no instante da pega e permanecem
        # fechados durante o transporte.
        set_finger_pose(fingers, FINGER_CLOSED_ROT, pick_frame)

        drop_point = final_center + Vector((0, 0, approach_height))
        claw.location = drop_point
        keyframe_lrs(claw, drop_frame, scale=False)
        set_finger_pose(fingers, FINGER_CLOSED_ROT, drop_frame)

        # Dedos abrem (soltam) logo após pousar a letra
        set_finger_pose(fingers, FINGER_OPEN_ROT, drop_frame + 8)

        retreat_point = drop_point + Vector((0, 0, 0.4))
        claw.location = retreat_point
        keyframe_lrs(claw, retreat_frame, scale=False)

    last_center = world_bbox_center(letters_with_offsets[-1][0])
    claw.location = last_center + Vector((0.8, -0.8, approach_height + 0.6))
    keyframe_lrs(claw, 360, scale=False)
    set_finger_pose(fingers, FINGER_OPEN_ROT, 360)


def animate_orb_beacon(orb, lamp, entry_frame, settle_frame, glow_frame, hold_frame, lights_collection):
    # Calcula o topo real da luminária (já com a escala aplicada) pela
    # caixa delimitadora, e pousa o orbe a uma distância fixa e uniforme
    # acima dela — em vez de um deslocamento fixo que desalinha quando a
    # luminária muda de tamanho.
    bpy.context.view_layer.update()
    corners = [lamp.matrix_world @ Vector(c) for c in lamp.bound_box]
    top_z = max(c.z for c in corners)
    center_x = sum(c.x for c in corners) / 8.0
    center_y = sum(c.y for c in corners) / 8.0
    GAP = 0.45
    target_world = Vector((center_x, center_y, top_z + GAP))

    orb.location = target_world
    final_loc = orb.location.copy()

    orb.location = final_loc + Vector((0.0, -1.3, 1.6))
    keyframe_lrs(orb, entry_frame, rot=False)

    orb.location = final_loc
    keyframe_lrs(orb, settle_frame, rot=False)
    keyframe_lrs(orb, hold_frame, rot=False)

    mat = orb.data.materials[0]
    bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    if "Emission Color" in bsdf.inputs and "Emission Strength" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (0.95, 0.63, 0.05, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
        bsdf.inputs["Emission Strength"].keyframe_insert(data_path="default_value", frame=settle_frame)
        bsdf.inputs["Emission Strength"].default_value = 6.0
        bsdf.inputs["Emission Strength"].keyframe_insert(data_path="default_value", frame=glow_frame)
        bsdf.inputs["Emission Strength"].keyframe_insert(data_path="default_value", frame=hold_frame)

    light_data = bpy.data.lights.new(name="Light_Farol_Orbe_Data", type='POINT')
    light_data.color = (0.95, 0.63, 0.05)
    light_data.energy = 0.0
    light_data.shadow_soft_size = 0.05
    light_obj = bpy.data.objects.new("Light_Farol_Orbe", light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    light_obj.parent = orb
    light_obj.location = (0.0, 0.0, 0.0)
    move_to_collection(light_obj, lights_collection)

    light_data.energy = 0.0
    light_data.keyframe_insert(data_path="energy", frame=settle_frame)
    light_data.energy = 120.0
    light_data.keyframe_insert(data_path="energy", frame=glow_frame)
    light_data.keyframe_insert(data_path="energy", frame=hold_frame)


def animate_camera(cam, pullback, lens_delta, settle_frame, hold_frame):
    final_loc = cam.location.copy()
    final_rot = cam.rotation_euler.copy()
    final_lens = cam.data.lens

    cam.location = final_loc + Vector(pullback)
    cam.data.lens = final_lens + lens_delta
    keyframe_lrs(cam, 1, scale=False)
    cam.data.keyframe_insert(data_path="lens", frame=1)

    cam.location = final_loc
    cam.data.lens = final_lens
    keyframe_lrs(cam, settle_frame, scale=False)
    cam.data.keyframe_insert(data_path="lens", frame=settle_frame)

    keyframe_lrs(cam, hold_frame, scale=False)
    cam.data.keyframe_insert(data_path="lens", frame=hold_frame)


# ===========================================================================
# RENDER
# ===========================================================================

def setup_render(scene):
    import os
    scene.frame_start = 1
    scene.frame_end = 360
    scene.render.fps = 24
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except TypeError:
        scene.render.engine = 'BLENDER_EEVEE'

    image_settings = scene.render.image_settings
    if hasattr(image_settings, "media_type"):
        image_settings.media_type = 'VIDEO'
    image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

    blend_dir = os.path.dirname(bpy.data.filepath) or "/tmp"
    scene.render.filepath = os.path.join(blend_dir, "AP2_NomeSobrenome.mp4")


# ===========================================================================
# EXECUÇÃO PRINCIPAL
# ===========================================================================

def main():
    clear_scene()
    scene = bpy.context.scene

    main_collection = get_or_create_collection("AP1_Ibmec_Conceito")
    lights_collection = get_or_create_collection("AC04_Luzes")

    mat_ibmec, _ = new_simple_material("MAT_Ibmec_Marca", (0.07, 0.12, 0.30, 1.0), 0.0, 0.35)
    letters = create_word_letters(main_collection, mat_ibmec)

    letter_I = letters["Letra_I"]
    letter_b = letters["Letra_b"]
    letter_m = letters["Letra_m"]
    letter_e = letters["Letra_e"]
    letter_c = letters["Letra_c"]

    # Luminária pousa exatamente no lugar/pé do "I" (a letra vai
    # desaparecer esmagada, então a sobreposição breve no instante do
    # impacto é intencional — é o "esmagamento").
    lamp_loc = (letter_I.location.x, -0.1, 0.0)
    lamp = create_lamp(main_collection, lamp_loc)
    mat_wood, _ = new_simple_material("MAT_Luminaria_Branca", (0.92, 0.92, 0.94, 1.0), 0.0, 0.4)
    lamp.data.materials.clear()
    lamp.data.materials.append(mat_wood)

    orb = create_orb(main_collection, (letter_I.location.x - 3.0, -2.0, 2.0))
    mat_mirror, _ = new_simple_material("MAT_Orbe_Laranja", (0.95, 0.63, 0.05, 1.0), 0.2, 0.15)
    orb.data.materials.clear()
    orb.data.materials.append(mat_mirror)

    claw, claw_fingers = create_claw(main_collection, (letter_I.location.x + 3.0, -2.0, 1.5))
    mat_metal, _ = new_simple_material("MAT_Metal_Escovado", (0.75, 0.76, 0.78, 1.0), 1.0, 0.25)
    for part in [claw] + claw_fingers:
        part.data.materials.clear()
        part.data.materials.append(mat_metal)

    word_center = Vector((0.0, 0.0, 0.3))
    cam = create_camera(main_collection, word_center)
    create_lights(lights_collection)
    create_backdrop(main_collection, word_center)
    enable_camera_dof(cam, word_center, main_collection)

    # --- Animação ---
    IMPACT = 50
    REBOUND = 70
    animate_lamp_squash(lamp, fall_from=(0.0, 0.0, 4.0), impact_frame=IMPACT, rebound_frame=REBOUND)
    # A letra "I" existe desde o início, visível e parada no lugar — a
    # luminária cai, a esmaga no impacto e ela some logo em seguida.
    animate_letter_crushed(letter_I, IMPACT)

    deliveries = [
        (letter_b, Vector((-1.4, 0.3, 2.2)), 90, 135, 145),
        (letter_m, Vector((0.0, -1.4, 2.4)), 150, 195, 205),
        (letter_e, Vector((1.4, 0.3, 2.2)), 210, 255, 265),
        (letter_c, Vector((2.0, 0.6, 1.9)), 270, 310, 320),
    ]
    animate_claw_delivering_letters(claw, claw_fingers, deliveries)

    animate_orb_beacon(orb, lamp,
                        entry_frame=320, settle_frame=350, glow_frame=360, hold_frame=360,
                        lights_collection=lights_collection)

    animate_camera(cam, pullback=(0.0, -2.2, 0.8), lens_delta=-10.0, settle_frame=330, hold_frame=360)

    setup_render(scene)
    scene.frame_current = 1

    print("Cena e animação criadas do zero com sucesso.")
    print(f"  Luminária esmaga o I no frame {IMPACT} (rebote até {REBOUND}).")
    print("  Garra entrega: b (90-145), m (150-205), e (210-265), c (270-320).")
    print("  Orbe sobe e brilha como farol (320-360).")
    print("Salve agora como AP2_NomeSobrenome.blend.")


if __name__ == "__main__":
    main()
