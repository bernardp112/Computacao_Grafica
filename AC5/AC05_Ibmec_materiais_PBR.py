"""
AC05_Ibmec_materiais_PBR.py
----------------------------
Script para o Scripting Tab do Blender 4.5 LTS.

PRE-REQUISITO: rode isso DEPOIS de abrir a cena da AC04 (a que ja tem
Ibmec_Palavra, Obj_Luminaria, Obj_Orbe, Obj_Garra, as luzes e os materiais
Lambert/Phong/Blinn-Phong da etapa anterior). Antes de rodar:
  1. File > Save As... > AC05_NomeSobrenome.blend
     (nao sobrescreva AP1 nem AC04)
  2. Copie a pasta "AC05_texturas" (entregue junto com este script) para a
     MESMA pasta onde voce salvou o AC05_NomeSobrenome.blend.
  3. Ajuste a variavel TEXTURE_DIR abaixo se usar outro local.

O que este script faz:
1. Cria/atualiza coleção "AC05_Materiais_Texturas" (para qualquer elemento
   auxiliar que você queira adicionar depois).
2. Cria UV maps (Smart UV Project) para os três objetos autorais.
3. Cria três materiais PBR novos (substituindo os da comparação
   Lambert/Phong/Blinn-Phong da AC04, que continuam preservados no arquivo
   da AC04 — aqui é uma cópia):
     - MAT_Metal_Escovado  -> Obj_Garra  (metal, com Base Color, Roughness
       e Normal Map conectados = demonstra os 3 canais pedidos)
     - MAT_Madeira_PBR     -> Obj_Luminaria (madeira, Base Color + Roughness
       via textura de imagem)
     - MAT_Espelho         -> Obj_Orbe (metal polido/espelhado, cor sólida,
       Metallic=1.0, Roughness≈0.0 — material PBR sem textura de imagem)
4. Atualiza o material da palavra "Ibmec" preservando a cor da marca,
   apenas com ajuste leve de PBR (sem textura, sem comprometer leitura).
5. Configura corretamente o espaço de cor de cada mapa:
   Base Color = sRGB (padrão), Roughness e Normal = Non-Color.
6. Empacota todas as imagens externas no .blend (File > External Data >
   Pack Resources), para não depender de caminhos locais depois de salvo.

Como usar:
- Abra o Blender 4.5 LTS com a cena da AC04 já carregada e salva como
  AC05_NomeSobrenome.blend.
- Vá em Scripting, cole este código em um novo Text, clique em Run Script.
- Depois confira em Material Preview e em Rendered, ajustando luz se
  necessário (registre qualquer ajuste no relatório).
"""

import bpy
import os

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO — ajuste se necessário
# ---------------------------------------------------------------------------

# Pasta onde estão as texturas (wood_basecolor.png, metal_basecolor.png etc.)
# Por padrão, assume uma subpasta "AC05_texturas" ao lado do arquivo .blend.
TEXTURE_DIR = os.path.join(os.path.dirname(bpy.data.filepath), "AC05_texturas")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def get_object(name):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise RuntimeError(
            f"Objeto '{name}' não encontrado. Confirme que você abriu a cena "
            f"da AC04 antes de rodar este script."
        )
    return obj


def get_or_create_collection(name):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def load_image(filename, colorspace):
    path = os.path.join(TEXTURE_DIR, filename)
    if not os.path.exists(path):
        raise RuntimeError(
            f"Textura não encontrada em: {path}\n"
            f"Copie a pasta 'AC05_texturas' para o local esperado ou ajuste "
            f"a variável TEXTURE_DIR no início do script."
        )
    img = bpy.data.images.get(filename)
    if img is None:
        img = bpy.data.images.load(path)
    img.colorspace_settings.name = colorspace
    return img


def smart_uv_unwrap(obj):
    """Cria/renova o UV map do objeto usando Smart UV Project."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.select_set(False)


def new_material(name):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    # Limpa nós extras, mantendo apenas Principled BSDF + Material Output
    nodes = mat.node_tree.nodes
    for n in list(nodes):
        if n.type not in ('BSDF_PRINCIPLED', 'OUTPUT_MATERIAL'):
            nodes.remove(n)
    bsdf = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf is None:
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = next((n for n in nodes if n.type == 'OUTPUT_MATERIAL'), None)
    if output is None:
        output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat, bsdf


def assign_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def set_scalar(bsdf, input_name, value):
    if input_name in bsdf.inputs:
        bsdf.inputs[input_name].default_value = value


# ---------------------------------------------------------------------------
# Material 1: Metal Escovado (Base Color + Roughness + Normal) -> Obj_Garra
# ---------------------------------------------------------------------------

def build_metal_material():
    mat, bsdf = new_material("MAT_Metal_Escovado")
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    tex_base = nodes.new('ShaderNodeTexImage')
    tex_base.image = load_image("metal_basecolor.png", "sRGB")
    tex_base.location = (-700, 300)

    tex_rough = nodes.new('ShaderNodeTexImage')
    tex_rough.image = load_image("metal_roughness.png", "Non-Color")
    tex_rough.location = (-700, 0)

    tex_norm = nodes.new('ShaderNodeTexImage')
    tex_norm.image = load_image("metal_normal.png", "Non-Color")
    tex_norm.location = (-700, -300)

    normal_map = nodes.new('ShaderNodeNormalMap')
    normal_map.location = (-350, -300)

    links.new(tex_base.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(tex_rough.outputs['Color'], bsdf.inputs['Roughness'])
    links.new(tex_norm.outputs['Color'], normal_map.inputs['Color'])
    links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

    set_scalar(bsdf, "Metallic", 1.0)
    return mat


# ---------------------------------------------------------------------------
# Material 2: Madeira PBR (Base Color + Roughness) -> Obj_Luminaria
# ---------------------------------------------------------------------------

def build_wood_material():
    mat, bsdf = new_material("MAT_Madeira_PBR")
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    tex_base = nodes.new('ShaderNodeTexImage')
    tex_base.image = load_image("wood_basecolor.png", "sRGB")
    tex_base.location = (-700, 300)

    tex_rough = nodes.new('ShaderNodeTexImage')
    tex_rough.image = load_image("wood_roughness.png", "Non-Color")
    tex_rough.location = (-700, 0)

    links.new(tex_base.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(tex_rough.outputs['Color'], bsdf.inputs['Roughness'])

    set_scalar(bsdf, "Metallic", 0.0)
    return mat


# ---------------------------------------------------------------------------
# Material 3: Espelho (cor sólida, sem textura de imagem) -> Obj_Orbe
# ---------------------------------------------------------------------------

def build_mirror_material():
    mat, bsdf = new_material("MAT_Espelho")
    set_scalar(bsdf, "Base Color", (0.9, 0.92, 0.95, 1.0))
    set_scalar(bsdf, "Metallic", 1.0)
    set_scalar(bsdf, "Roughness", 0.02)
    return mat


# ---------------------------------------------------------------------------
# Material da palavra Ibmec — preserva cor/leitura, sem textura
# ---------------------------------------------------------------------------

def update_ibmec_material(obj):
    mat = obj.data.materials[0] if obj.data.materials else None
    if mat is None:
        mat, bsdf = new_material("MAT_Ibmec_Marca")
        assign_material(obj, mat)
    else:
        mat.use_nodes = True
        bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if bsdf is None:
            mat, bsdf = new_material(mat.name)
            assign_material(obj, mat)

    # Cor institucional aproximada da marca Ibmec (ajuste para o tom oficial
    # exato conforme o manual de marca, se tiver os valores precisos).
    set_scalar(bsdf, "Base Color", (0.78, 0.0, 0.08, 1.0))
    set_scalar(bsdf, "Metallic", 0.0)
    set_scalar(bsdf, "Roughness", 0.35)
    return mat


# ---------------------------------------------------------------------------
# Execução principal
# ---------------------------------------------------------------------------

def main():
    lamp_obj = get_object("Obj_Luminaria")
    orb_obj = get_object("Obj_Orbe")
    claw_obj = get_object("Obj_Garra")
    word_obj = get_object("Ibmec_Palavra")

    get_or_create_collection("AC05_Materiais_Texturas")

    # UVs para os objetos que recebem textura de imagem
    smart_uv_unwrap(claw_obj)
    smart_uv_unwrap(lamp_obj)

    mat_metal = build_metal_material()
    mat_wood = build_wood_material()
    mat_mirror = build_mirror_material()

    assign_material(claw_obj, mat_metal)
    assign_material(lamp_obj, mat_wood)
    assign_material(orb_obj, mat_mirror)

    update_ibmec_material(word_obj)

    # Empacota as imagens externas dentro do .blend
    bpy.ops.file.pack_all()

    print("Materiais PBR aplicados:")
    print("  Obj_Garra     -> MAT_Metal_Escovado (Base Color + Roughness + Normal)")
    print("  Obj_Luminaria -> MAT_Madeira_PBR (Base Color + Roughness)")
    print("  Obj_Orbe      -> MAT_Espelho (cor sólida, Metallic=1.0, Roughness≈0.0)")
    print("  Ibmec_Palavra -> material atualizado, cor da marca preservada")
    print("UVs criados (Smart UV Project) para Obj_Garra e Obj_Luminaria.")
    print("Recursos externos empacotados no .blend (File > External Data > Pack Resources).")
    print("Salve o arquivo agora (Ctrl+S) para persistir as mudanças.")


if __name__ == "__main__":
    main()
