"""
AP1_Ibmec_setup.py
-------------------
Script para o Scripting Tab do Blender 4.5 LTS.

O que este script faz:
1. Limpa a cena atual (cuidado: apague/salve seu .blend antes de rodar,
   ou rode em um arquivo novo).
2. Cria a coleção principal "AP1_Ibmec_Conceito".
3. Cria a palavra "Ibmec" como texto convertido em malha (com extrude + bevel).
4. Cria os três objetos autorais: luminária articulada, orbe estilizado e
   garra mecânica — todos modelados com primitivas + pelo menos duas
   técnicas de modelagem além de escala simples (bevel, inset, subdivide,
   modificador Subsurf, modificador Mirror).
5. Cria a câmera principal, pronta para animação na AP2.
6. Configura a cena para 24 fps e 360 frames (15s).

IMPORTANTE: as posições/rotações são um PONTO DE PARTIDA aproximado.
Depois de rodar o script, ajuste manualmente no viewport (G/R/S) a posição
de cada objeto em relação às letras "I", "i" (ponto) e "C" até ficar como
você imaginou (lâmpada esmagando o I, orbe no ponto do i, garra formando o C).

Como usar:
- Abra o Blender 4.5 LTS.
- Vá em Scripting (aba superior).
- Cole este código em um novo Text (New) ou abra este arquivo .py.
- Clique em "Run Script" (ícone de play).
"""

import bpy
import math


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def clear_scene():
    """Remove todos os objetos da cena atual e limpa dados órfãos."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.curves):
        if block.users == 0:
            bpy.data.curves.remove(block)


def get_or_create_collection(name):
    """Cria (ou reaproveita) a coleção principal do projeto."""
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def move_to_collection(obj, collection):
    """Garante que 'obj' esteja apenas dentro de 'collection'."""
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection.objects.link(obj)


def edit_mode_select_all_and(op_callable):
    """Entra em Edit Mode, seleciona tudo, executa uma operação e volta."""
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    op_callable()
    bpy.ops.object.mode_set(mode='OBJECT')


# ---------------------------------------------------------------------------
# Palavra IBMEC (texto convertido em malha)
# ---------------------------------------------------------------------------

def create_word_ibmec(collection):
    curve_data = bpy.data.curves.new(name="Ibmec_Curve", type='FONT')
    curve_data.body = "Ibmec"
    curve_data.extrude = 0.08          # dá volume à letra (profundidade)
    curve_data.bevel_depth = 0.015     # arredonda as bordas da letra
    curve_data.bevel_resolution = 3
    curve_data.align_x = 'CENTER'
    curve_data.align_y = 'CENTER'
    curve_data.size = 1.6

    obj = bpy.data.objects.new("Ibmec_Palavra", curve_data)
    bpy.context.scene.collection.objects.link(obj)
    move_to_collection(obj, collection)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')  # transforma o texto em malha editável
    obj.select_set(False)

    obj.location = (0, 0, 0)
    return obj


# ---------------------------------------------------------------------------
# Objeto autoral 1: Luminária articulada (esmaga o "I")
# ---------------------------------------------------------------------------

def create_lamp(collection, location=(-2.6, 0.0, 0.0)):
    lx, ly, lz = location
    parts = []

    bpy.ops.mesh.primitive_cylinder_add(radius=0.30, depth=0.14,
                                         location=(lx, ly, lz + 0.07))
    base = bpy.context.object
    base.name = "Lamp_Base"
    parts.append(base)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.9,
                                         location=(lx, ly, lz + 0.55))
    arm1 = bpy.context.object
    arm1.rotation_euler = (math.radians(15), 0, 0)
    arm1.name = "Lamp_Arm1"
    parts.append(arm1)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07,
                                          location=(lx, ly - 0.12, lz + 0.98))
    joint = bpy.context.object
    joint.name = "Lamp_Joint"
    # Bevel nas arestas da junta (recurso de modelagem extra)
    bpy.context.view_layer.objects.active = joint
    edit_mode_select_all_and(
        lambda: bpy.ops.mesh.bevel(offset=0.01, segments=2, affect='EDGES')
    )
    parts.append(joint)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.85,
                                         location=(lx - 0.05, ly - 0.5, lz + 1.3))
    arm2 = bpy.context.object
    arm2.rotation_euler = (math.radians(-65), 0, 0)
    arm2.name = "Lamp_Arm2"
    parts.append(arm2)

    bpy.ops.mesh.primitive_cone_add(radius1=0.20, radius2=0.05, depth=0.28,
                                     location=(lx - 0.05, ly - 0.9, lz + 1.55),
                                     rotation=(math.radians(100), 0, 0))
    dome = bpy.context.object
    dome.name = "Lamp_Dome"
    # Modificador Subdivision Surface para suavizar a cúpula (recurso extra)
    mod = dome.modifiers.new(name="Subsurf", type='SUBSURF')
    mod.levels = 2
    mod.render_levels = 2
    parts.append(dome)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()

    lamp_obj = bpy.context.object
    lamp_obj.name = "Obj_Luminaria"
    move_to_collection(lamp_obj, collection)
    return lamp_obj


# ---------------------------------------------------------------------------
# Objeto autoral 2: Orbe estilizado (ponto do "i")
# ---------------------------------------------------------------------------

def create_orb(collection, location=(-0.75, 0.0, 1.55)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.16,
                                           location=location)
    orb = bpy.context.object
    orb.name = "Orb_Core"

    # Inset Faces cria padrão facetado na superfície (recurso de modelagem extra)
    bpy.context.view_layer.objects.active = orb
    edit_mode_select_all_and(
        lambda: bpy.ops.mesh.inset(thickness=0.012, depth=0.0)
    )

    rings = [orb]
    ring_rotations = [(0, 0, 0), (math.radians(60), 0, 0), (0, math.radians(60), 0)]
    for i, rot in enumerate(ring_rotations):
        bpy.ops.mesh.primitive_torus_add(location=location, rotation=rot,
                                          major_radius=0.22, minor_radius=0.01,
                                          major_segments=24, minor_segments=8)
        ring = bpy.context.object
        ring.name = f"Orb_Ring_{i + 1}"
        rings.append(ring)

    bpy.ops.object.select_all(action='DESELECT')
    for r in rings:
        r.select_set(True)
    bpy.context.view_layer.objects.active = orb
    bpy.ops.object.join()

    orb_obj = bpy.context.object
    orb_obj.name = "Obj_Orbe"
    move_to_collection(orb_obj, collection)
    return orb_obj


# ---------------------------------------------------------------------------
# Objeto autoral 3: Garra mecânica (forma o "C")
# ---------------------------------------------------------------------------

def create_claw(collection, location=(2.9, 0.0, 0.9)):
    lx, ly, lz = location

    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.35,
                                         location=(lx, ly, lz))
    hub = bpy.context.object
    hub.name = "Claw_Hub"

    fingers = [hub]
    finger_offsets = [(-0.13, 0.0), (0.0, 0.15), (0.13, 0.0)]
    for i, (dx, dy) in enumerate(finger_offsets):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.032, depth=0.5,
            location=(lx + dx, ly + dy, lz - 0.35)
        )
        finger = bpy.context.object
        finger.name = f"Claw_Finger_{i + 1}"

        bpy.context.view_layer.objects.active = finger
        # Subdivide cria "juntas" no dedo (equivalente a loop cuts)
        edit_mode_select_all_and(lambda: bpy.ops.mesh.subdivide(number_cuts=2))
        # Bevel arredonda as pontas/arestas dos dedos (recurso extra)
        edit_mode_select_all_and(
            lambda: bpy.ops.mesh.bevel(offset=0.008, segments=2, affect='EDGES')
        )

        fingers.append(finger)

    bpy.ops.object.select_all(action='DESELECT')
    for f in fingers:
        f.select_set(True)
    bpy.context.view_layer.objects.active = hub
    bpy.ops.object.join()

    claw_obj = bpy.context.object
    claw_obj.name = "Obj_Garra"

    # Modificador Mirror para simetrizar os dedos (recurso extra)
    mirror_mod = claw_obj.modifiers.new(name="Mirror", type='MIRROR')
    mirror_mod.use_axis[0] = True
    mirror_mod.use_axis[1] = False
    mirror_mod.use_axis[2] = False

    move_to_collection(claw_obj, collection)
    return claw_obj


# ---------------------------------------------------------------------------
# Câmera principal
# ---------------------------------------------------------------------------

def create_camera(collection):
    cam_data = bpy.data.cameras.new("Camera_Principal_Data")
    cam_data.lens = 50

    cam_obj = bpy.data.objects.new("Camera_Principal", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    move_to_collection(cam_obj, collection)

    cam_obj.location = (0.0, -8.0, 1.0)
    cam_obj.rotation_euler = (math.radians(90), 0.0, 0.0)

    bpy.context.scene.camera = cam_obj
    return cam_obj


# ---------------------------------------------------------------------------
# Configuração de cena (15s a 24 fps = 360 frames)
# ---------------------------------------------------------------------------

def setup_scene():
    scene = bpy.context.scene
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = 360
    scene.frame_current = 1


# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------

def main():
    clear_scene()
    collection = get_or_create_collection("AP1_Ibmec_Conceito")

    create_word_ibmec(collection)

    lamp = create_lamp(collection, location=(-2.6, 0.0, 0.0))
    lamp.rotation_euler = (0.0, 0.0, math.radians(-12))

    create_orb(collection, location=(-0.75, 0.0, 1.55))

    claw = create_claw(collection, location=(2.9, 0.0, 0.9))
    claw.rotation_euler = (0.0, 0.0, math.radians(8))

    create_camera(collection)
    setup_scene()

    print("Cena 'AP1_Ibmec_Conceito' criada com sucesso.")
    print("Ajuste manualmente as posições dos objetos em relação às letras,")
    print("depois salve como AP1_NomeSobrenome.blend.")


if __name__ == "__main__":
    main()
