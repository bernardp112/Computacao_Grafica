# Relatório AC05 — Materiais PBR e Texturas

**Aluno(a):** [Seu Nome Completo]
**Disciplina:** [Nome da disciplina]
**Software:** Blender 4.5 LTS
**Arquivo:** AC05_NomeSobrenome.blend (cópia da cena da AC04, originais da AP1 e AC04 preservados)

---

## 1. Continuidade da AP1/AC04

A cena foi reaberta a partir do arquivo da AC04 e salva como cópia (`AC05_NomeSobrenome.blend`), sem sobrescrever os arquivos da AP1 ou da AC04. A composição, o enquadramento da câmera principal e a iluminação (`Light_Principal` e `Light_Preenchimento`) foram mantidos como ponto de partida. A palavra "Ibmec" permanece legível e com sua cor de marca preservada; nenhuma textura, relevo ou efeito foi aplicado a ela — apenas um ajuste leve de propriedades PBR (Roughness) no material já existente.

## 2. Identificação dos três objetos e descrição dos materiais aplicados

| Objeto autoral | Material | Tipo de superfície | Mapas de imagem usados |
|---|---|---|---|
| `Obj_Garra` | `MAT_Metal_Escovado` | Metal escovado | Base Color, Roughness e Normal (textura de imagem) |
| `Obj_Luminaria` | `MAT_Madeira_PBR` | Madeira | Base Color e Roughness (textura de imagem) |
| `Obj_Orbe` | `MAT_Espelho` | Metal polido/espelhado | Nenhum — cor sólida + Metallic/Roughness |

A garra (metal escovado) e a luminária (madeira) foram escolhidas por coerência com o conceito da AP1: a garra remete a precisão/engenharia (metal) e a luminária a construção/solidez (madeira como base, mantendo o restante da forma). O orbe recebeu um acabamento espelhado para reforçar a ideia de "destaque" e reflexo do ambiente, sem precisar de textura de imagem — demonstrando que um material PBR identificável também pode ser construído só com cor sólida e os parâmetros Metallic/Roughness.

## 3. Propriedades principais de cada material

| Material | Base Color | Metallic | Roughness | Normal |
|---|---|---|---|---|
| MAT_Metal_Escovado | textura `metal_basecolor.png` | 1.0 | textura `metal_roughness.png` (~0.15–0.35) | textura `metal_normal.png` via nó Normal Map |
| MAT_Madeira_PBR | textura `wood_basecolor.png` | 0.0 | textura `wood_roughness.png` (~0.55–0.85) | — |
| MAT_Espelho | cor sólida (0.9, 0.92, 0.95) | 1.0 | 0.02 | — |
| Material da palavra Ibmec | cor da marca (0.78, 0.0, 0.08) | 0.0 | 0.35 | — |

## 4. Mapas utilizados e como foram conectados

No material `MAT_Metal_Escovado` os três canais pedidos foram demonstrados:
- **Base Color/Albedo** → nó *Image Texture* (`metal_basecolor.png`, espaço de cor **sRGB**) → entrada *Base Color* do Principled BSDF.
- **Roughness** → nó *Image Texture* (`metal_roughness.png`, espaço de cor **Non-Color**, por ser mapa de dados) → entrada *Roughness*.
- **Normal** → nó *Image Texture* (`metal_normal.png`, espaço de cor **Non-Color**) → nó **Normal Map** → entrada *Normal* do Principled BSDF.

No material `MAT_Madeira_PBR`, Base Color (sRGB) e Roughness (Non-Color) seguem a mesma lógica, sem mapa Normal (opcional, não utilizado por não ser necessário para o nível de detalhe da madeira nesta etapa). O mapa Metallic não foi usado em nenhum material por meio de textura — os valores de metalicidade foram definidos manualmente (0.0 para não-metais, 1.0 para metais), conforme recomendado no enunciado.

## 5. Método de UV e ajustes para reduzir distorções

Para `Obj_Garra` e `Obj_Luminaria` (os dois objetos com textura de imagem) foi usado **Smart UV Project** (ângulo-limite 66°, margem entre ilhas de 0.02), por ser um método rápido e adequado para objetos compostos por múltiplas primitivas unidas (join), evitando distorções fortes em superfícies com ângulos variados. Após o unwrap, as ilhas foram inspecionadas no UV Editor; como as texturas usadas (madeira e metal escovado) são padrões repetitivos e não possuem elementos que exijam alinhamento exato (como um logotipo), pequenas distorções/rotações entre ilhas não comprometem a leitura do material. Caso a textura real usada pelo aluno tenha padrão direcional importante, recomenda-se revisar manualmente a orientação das ilhas no UV Editor e ajustar com *Follow Active Quads* ou unwrap manual por partes.

## 6. Origem e licença das texturas

Todas as texturas de imagem (`wood_basecolor.png`, `wood_roughness.png`, `metal_basecolor.png`, `metal_roughness.png`, `metal_normal.png`) foram **geradas proceduralmente por script Python** (NumPy + PIL), especificamente para este projeto — não são fotografias nem texturas de bancos de imagens de terceiros. Por serem criações originais do autor deste trabalho, não há restrição de licença associada ao uso dessas imagens. Os arquivos foram empacotados dentro do `.blend` (File > External Data > Pack Resources) para que o projeto não dependa de caminhos locais.

## 7. Influência da iluminação sobre os materiais

Sob a iluminação herdada da AC04 (`Light_Principal`, Area, em ângulo, + `Light_Preenchimento`, Sun fraca):
- O **metal escovado** (`Obj_Garra`) apresenta highlight especular concentrado e alongado na direção das linhas do padrão escovado, com leve variação de brilho conforme o ângulo de observação — efeito reforçado pelo mapa Normal, que cria microvariações perceptíveis na superfície mesmo com geometria lisa.
- A **madeira** (`Obj_Luminaria`) absorve mais luz difusa e não produz highlight concentrado, devido à rugosidade alta (~0.55–0.85); o padrão de veios fica visível principalmente pela variação de cor (Base Color), não por reflexo.
- O **espelho** (`Obj_Orbe`) reflete fortemente o ambiente e a luz principal, produzindo um reflexo nítido e de alto contraste — o comportamento esperado para Metallic=1.0 e Roughness≈0.02.
- Não foi necessário alterar a posição ou intensidade das luzes da AC04 para que os três materiais ficassem legíveis; apenas a troca do modo de visualização do viewport para *Rendered* foi usada para conferência.

---
*Imagens relacionadas: render final pela câmera principal (`AC05_render_final.png`), captura do Shader Editor do material `MAT_Metal_Escovado` (`AC05_shader_editor.png`) e captura do UV Editor de `Obj_Garra` ou `Obj_Luminaria` (`AC05_uv_editor.png`).*
