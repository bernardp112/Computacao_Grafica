import bpy
import math
from mathutils import Vector

# ============================================================
# AC03 - PARQUE GEOMÉTRICO
# Blender 4.5 LTS
# ============================================================


# ============================================================
# 1. LIMPEZA DA CENA
# ============================================================

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Remove a coleção anterior, se existir
colecao_antiga = bpy.data.collections.get("AC03_transformacoes")

if colecao_antiga:
    bpy.data.collections.remove(colecao_antiga)


# ============================================================
# 2. CRIAÇÃO DA COLEÇÃO
# ============================================================

colecao = bpy.data.collections.new("AC03_transformacoes")
bpy.context.scene.collection.children.link(colecao)


# Função para mover objetos para a coleção
def mover_para_colecao(obj):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)

    colecao.objects.link(obj)


# ============================================================
# 3. CONFIGURAÇÃO DA CENA
# ============================================================

scene = bpy.context.scene

scene.frame_start = 1
scene.frame_end = 120
scene.render.fps = 24


# ============================================================
# 4. OBJETOS 2D
# ============================================================

# ------------------------------------------------------------
# QUADRADO
# ------------------------------------------------------------

bpy.ops.mesh.primitive_plane_add(
    size=2,
    location=(-3, 0, 0)
)

quadrado = bpy.context.active_object
quadrado.name = "obj2d_quadrado"

mover_para_colecao(quadrado)

quadrado.scale = (
    1.4,
    1.0,
    1.0
)

quadrado.rotation_euler = (
    0,
    0,
    math.radians(25)
)


# ------------------------------------------------------------
# TRIÂNGULO
# ------------------------------------------------------------

bpy.ops.mesh.primitive_circle_add(
    vertices=3,
    radius=1.2,
    fill_type='TRIFAN',
    location=(0, 0, 0.02)
)

triangulo = bpy.context.active_object
triangulo.name = "obj2d_triangulo"

mover_para_colecao(triangulo)

triangulo.scale = (
    1.2,
    1.0,
    1.0
)

triangulo.rotation_euler = (
    0,
    0,
    math.radians(30)
)


# ------------------------------------------------------------
# CÍRCULO
# ------------------------------------------------------------

bpy.ops.mesh.primitive_circle_add(
    vertices=32,
    radius=1.1,
    fill_type='NGON',
    location=(3, 0, 0.02)
)

circulo = bpy.context.active_object
circulo.name = "obj2d_circulo"

mover_para_colecao(circulo)

circulo.scale = (
    1.2,
    1.2,
    1.0
)

circulo.rotation_euler = (
    0,
    0,
    math.radians(15)
)


# ============================================================
# 5. OBJETOS 3D
# ============================================================

# ------------------------------------------------------------
# CUBO
# ------------------------------------------------------------

bpy.ops.mesh.primitive_cube_add(
    location=(-3, 3, 1)
)

cubo = bpy.context.active_object
cubo.name = "obj3d_cubo"

mover_para_colecao(cubo)

cubo.scale = (
    1.2,
    0.8,
    1.5
)

cubo.rotation_euler = (
    math.radians(25),
    math.radians(15),
    math.radians(40)
)


# ------------------------------------------------------------
# CILINDRO
# ------------------------------------------------------------

bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=1,
    depth=2,
    location=(0, 3, 1)
)

cilindro = bpy.context.active_object
cilindro.name = "obj3d_cilindro"

mover_para_colecao(cilindro)

cilindro.scale = (
    0.8,
    0.8,
    1.4
)

cilindro.rotation_euler = (
    math.radians(15),
    math.radians(30),
    math.radians(20)
)


# ------------------------------------------------------------
# ESFERA UV
# ------------------------------------------------------------

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=32,
    ring_count=16,
    radius=1,
    location=(3, 3, 1)
)

esfera = bpy.context.active_object
esfera.name = "obj3d_esfera"

mover_para_colecao(esfera)

esfera.scale = (
    1.0,
    1.3,
    0.9
)

esfera.rotation_euler = (
    math.radians(20),
    math.radians(35),
    math.radians(45)
)


# ============================================================
# 6. ANIMAÇÃO DO QUADRADO
# Translação + rotação
# ============================================================

# FRAME 1
scene.frame_set(1)

quadrado.location = (
    -3,
    0,
    0
)

quadrado.rotation_euler = (
    0,
    0,
    math.radians(25)
)

quadrado.keyframe_insert(
    data_path="location",
    frame=1
)

quadrado.keyframe_insert(
    data_path="rotation_euler",
    frame=1
)


# FRAME 120
scene.frame_set(120)

quadrado.location = (
    2,
    1,
    0
)

quadrado.rotation_euler = (
    0,
    0,
    math.radians(180)
)

quadrado.keyframe_insert(
    data_path="location",
    frame=120
)

quadrado.keyframe_insert(
    data_path="rotation_euler",
    frame=120
)


# ============================================================
# 7. ANIMAÇÃO DO CUBO
# Escala + rotação
# ============================================================

# FRAME 1
scene.frame_set(1)

cubo.scale = (
    1.2,
    0.8,
    1.5
)

cubo.rotation_euler = (
    math.radians(25),
    math.radians(15),
    math.radians(40)
)

cubo.keyframe_insert(
    data_path="scale",
    frame=1
)

cubo.keyframe_insert(
    data_path="rotation_euler",
    frame=1
)


# FRAME 120
scene.frame_set(120)

cubo.scale = (
    1.8,
    0.6,
    1.0
)

cubo.rotation_euler = (
    math.radians(90),
    math.radians(45),
    math.radians(120)
)

cubo.keyframe_insert(
    data_path="scale",
    frame=120
)

cubo.keyframe_insert(
    data_path="rotation_euler",
    frame=120
)


# ============================================================
# 8. PLANO BASE
# ============================================================

bpy.ops.mesh.primitive_plane_add(
    size=12,
    location=(0, 1.5, -0.05)
)

base = bpy.context.active_object
base.name = "base_parque"

mover_para_colecao(base)


# ============================================================
# 9. CÂMERA
# ============================================================

bpy.ops.object.camera_add(
    location=(10, -12, 11)
)

camera = bpy.context.active_object
camera.name = "camera_parque"

mover_para_colecao(camera)

# ------------------------------------------------------------
# Define o ponto para onde a câmera vai olhar
# ------------------------------------------------------------

alvo = Vector((0.0, 1.5, 0.8))

# Agora os dois valores são Vector
direcao = alvo - camera.location

# Rotaciona a câmera para olhar para o alvo
camera.rotation_euler = (
    direcao.to_track_quat('-Z', 'Y').to_euler()
)

# Distância focal
camera.data.lens = 50

# Define a câmera como câmera ativa
scene.camera = camera


# ============================================================
# 10. LUZ PRINCIPAL
# ============================================================

bpy.ops.object.light_add(
    type='AREA',
    location=(2, -2, 10)
)

luz = bpy.context.active_object
luz.name = "luz_principal"

mover_para_colecao(luz)

luz.data.energy = 1200
luz.data.shape = 'DISK'
luz.data.size = 8


# ============================================================
# 11. SEGUNDA LUZ
# ============================================================

bpy.ops.object.light_add(
    type='AREA',
    location=(-5, 4, 6)
)

luz2 = bpy.context.active_object
luz2.name = "luz_secundaria"

mover_para_colecao(luz2)

luz2.data.energy = 700
luz2.data.shape = 'DISK'
luz2.data.size = 5


# ============================================================
# 12. CONFIGURAÇÕES DO RENDER
# ============================================================

scene.render.resolution_x = 800
scene.render.resolution_y = 600
scene.render.resolution_percentage = 100

scene.render.image_settings.file_format = 'PNG'

# Define o frame inicial
scene.frame_set(1)


# ============================================================
# 13. VERIFICAÇÃO DA CÂMERA
# ============================================================

if scene.camera is None:

    print("ERRO: nenhuma câmera foi encontrada!")

else:

    print("Câmera ativa:", scene.camera.name)


# ============================================================
# 14. MENSAGEM FINAL
# ============================================================

print("")
print("==========================================")
print("       AC03 - PARQUE GEOMÉTRICO")
print("==========================================")
print("")
print("OBJETOS 2D:")
print(" - obj2d_quadrado")
print(" - obj2d_triangulo")
print(" - obj2d_circulo")
print("")
print("OBJETOS 3D:")
print(" - obj3d_cubo")
print(" - obj3d_cilindro")
print(" - obj3d_esfera")
print("")
print("ANIMAÇÃO:")
print(" - Quadrado: translação + rotação")
print(" - Cubo: escala + rotação")
print(" - Frames: 1 a 120")
print(" - FPS: 24")
print(" - Duração: 5 segundos")
print("")
print("CÂMERA:", scene.camera.name)
print("")
print("SCRIPT EXECUTADO COM SUCESSO!")
print("==========================================")
