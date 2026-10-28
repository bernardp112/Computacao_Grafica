"""
AC04_Ibmec_materiais_luz.py
----------------------------
Script para o Scripting Tab do Blender 4.5 LTS.

PRÉ-REQUISITO: rode isso DEPOIS de abrir a cena da AP1 (a que já tem a
coleção "AP1_Ibmec_Conceito" com Ibmec_Palavra, Obj_Luminaria, Obj_Orbe e
Obj_Garra). Antes de rodar:
  File > Save As... > AC04_NomeSobrenome.blend
(para não sobrescrever o arquivo original da AP1).

O que este script faz:
1. Cria os três materiais MAT_Lambert, MAT_Phong e MAT_BlinnPhong
   (aproximações via Principled BSDF, como pedido no enunciado).
2. Aplica cada material a um dos três objetos autorais:
     Obj_Luminaria -> MAT_Lambert
     Obj_Orbe      -> MAT_Phong
     Obj_Garra     -> MAT_BlinnPhong
3. Cria uma luz principal (Area) e uma luz de preenchimento (Sun fraca),
   organizadas numa coleção "AC04_Luzes".
4. Troca o shading do viewport ativo para Rendered, para facilitar a
   conferência imediata.

NÃO mexe na palavra Ibmec nem na composição/posições definidas na AP1.

Como usar:
- Abra o Blender 4.5 LTS com a cena da AP1 já carregada.
- Salve uma cópia como AC04_NomeSobrenome.blend.
- Vá em Scripting, cole este código em um novo Text, clique em Run Script.
- Depois ajuste manualmente luz/câmera se quiser refinar antes do render.
"""

import bpy


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def get_object(name):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise RuntimeError(
            f"Objeto '{name}' não encontrado. Confirme que você abriu a cena "
            f"da AP1 antes de rodar este script."
        )
    return obj


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


# ---------------------------------------------------------------------------
# Materiais (Lambert / Phong / Blinn-Phong — aproximações via Principled BSDF)
# ---------------------------------------------------------------------------

def create_material(name, base_color, roughness, specular_value):
    """
    base_color: tupla RGBA (0-1)
    roughness: 0 (polido) a 1 (fosco)
    specular_value: intensidade do brilho especular.
        Tenta usar o input 'Specular IOR Level' (Blender 4.x novo nome);
        se não existir, cai para 'Specular'.
    """
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is None:
        # fallback: procura qualquer Principled BSDF nos nós
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                bsdf = node
                break

    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Roughness"].default_value = roughness

    # Blender 4.x renomeou "Specular" para "Specular IOR Level" no Principled BSDF.
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = specular_value
    elif "Specular" in bsdf.inputs:
        bsdf.inputs["Specular"].default_value = specular_value

    return mat


def assign_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def create_all_materials():
    # Lambert: fosco, quase sem especular. Rugosidade alta.
    mat_lambert = create_material(
        "MAT_Lambert",
        base_color=(0.75, 0.15, 0.15, 1.0),   # vermelho fosco
        roughness=1.0,
        specular_value=0.05,
    )

    # Phong: polido, brilho especular moderado. Rugosidade baixa.
    mat_phong = create_material(
        "MAT_Phong",
        base_color=(0.10, 0.45, 0.80, 1.0),   # azul
        roughness=0.2,
        specular_value=0.5,
    )

    # Blinn-Phong: polido, brilho especular mais intenso/concentrado.
    mat_blinnphong = create_material(
        "MAT_BlinnPhong",
        base_color=(0.15, 0.65, 0.30, 1.0),   # verde
        roughness=0.1,
        specular_value=0.9,
    )

    return mat_lambert, mat_phong, mat_blinnphong


# ---------------------------------------------------------------------------
# Iluminação
# ---------------------------------------------------------------------------

def create_lights(collection):
    # Luz principal (Area) — posicionada em ângulo para gerar sombras
    # e highlights perceptíveis nos três objetos autorais.
    key_data = bpy.data.lights.new(name="Light_Key_Data", type='AREA')
    key_data.energy = 400.0
    key_data.size = 1.5
    key_data.color = (1.0, 0.98, 0.92)  # leve tom quente

    key_obj = bpy.data.objects.new("Light_Principal", key_data)
    bpy.context.scene.collection.objects.link(key_obj)
    move_to_collection(key_obj, collection)
    key_obj.location = (-1.5, -4.0, 3.5)
    key_obj.rotation_euler = (0.9, 0.0, -0.4)

    # Luz de preenchimento (Sun, baixa intensidade) — suaviza sombras
    # sem competir com a luz principal.
    fill_data = bpy.data.lights.new(name="Light_Fill_Data", type='SUN')
    fill_data.energy = 0.6
    fill_data.color = (0.85, 0.9, 1.0)  # leve tom frio

    fill_obj = bpy.data.objects.new("Light_Preenchimento", fill_data)
    bpy.context.scene.collection.objects.link(fill_obj)
    move_to_collection(fill_obj, collection)
    fill_obj.rotation_euler = (1.0, 0.0, 2.3)

    return key_obj, fill_obj


# ---------------------------------------------------------------------------
# Viewport em Rendered (facilita conferência visual)
# ---------------------------------------------------------------------------

def set_viewport_rendered():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'


# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------

def main():
    lamp_obj = get_object("Obj_Luminaria")
    orb_obj = get_object("Obj_Orbe")
    claw_obj = get_object("Obj_Garra")

    mat_lambert, mat_phong, mat_blinnphong = create_all_materials()

    assign_material(lamp_obj, mat_lambert)
    assign_material(orb_obj, mat_phong)
    assign_material(claw_obj, mat_blinnphong)

    lights_collection = get_or_create_collection("AC04_Luzes")
    create_lights(lights_collection)

    set_viewport_rendered()

    print("Materiais aplicados:")
    print("  Obj_Luminaria -> MAT_Lambert")
    print("  Obj_Orbe      -> MAT_Phong")
    print("  Obj_Garra     -> MAT_BlinnPhong")
    print("Luzes 'Light_Principal' e 'Light_Preenchimento' criadas em AC04_Luzes.")
    print("Ajuste posição/intensidade da luz se necessário e faça o render de teste (F12).")


if __name__ == "__main__":
    main()
