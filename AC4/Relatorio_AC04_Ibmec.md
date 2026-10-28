# Relatório AC04 — Modelos de Iluminação (Lambert, Phong, Blinn-Phong)

**Aluno(a):** Bernardo de Souza Silva
**Disciplina:** Computação Gráfica
**Software:** Blender 4.5 LTS
**Arquivo:** AC04_BernardoSouza.blend (cópia da cena da AP1, original preservado)

---

## 1. Continuidade da AP1

A cena desenvolvida na AP1 (coleção `AP1_Ibmec_Conceito`) foi reaberta e salva como cópia (`AC04_BernardoSouza.blend`), sem alterar o arquivo original da AP1. A palavra "Ibmec" não sofreu nenhuma alteração de identidade visual, posição ou geometria — apenas os três objetos autorais e a iluminação foram modificados nesta etapa.

## 2. Identificação dos três objetos e material aplicado

| Objeto autoral | Material aplicado | Cor-base | Acabamento |
|---|---|---|---|
| `Obj_Luminaria` | `MAT_Lambert` | Vermelho (0.75, 0.15, 0.15) | Fosco, sem brilho especular evidente |
| `Obj_Orbe` | `MAT_Phong` | Azul (0.10, 0.45, 0.80) | Polido, brilho especular moderado e concentrado |
| `Obj_Garra` | `MAT_BlinnPhong` | Verde (0.15, 0.65, 0.30) | Polido, brilho especular mais intenso |

Cada material foi aplicado a um único objeto autoral, de modo que os três modelos de iluminação pudessem ser comparados simultaneamente sob a mesma luz.

## 3. Configuração da iluminação

- **Luz principal (`Light_Principal`):** tipo *Area*, energia 400 W, tamanho 1.5 m, cor levemente quente (1.0, 0.98, 0.92). Posicionada em ângulo (acima e à frente, deslocada lateralmente) para gerar sombras perceptíveis e highlights visíveis nos três objetos sem iluminação frontal plana.
- **Luz de preenchimento (`Light_Preenchimento`):** tipo *Sun*, energia 0.6, cor levemente fria (0.85, 0.9, 1.0). Usada apenas para suavizar as sombras mais escuras, sem competir com a luz principal nem gerar highlights próprios perceptíveis.
- A posição, intensidade e cor de ambas as luzes, assim como o enquadramento da câmera (`Camera_Principal`, herdada da AP1), foram mantidas idênticas durante todas as comparações entre os três materiais.

## 4. Valores principais de cada material

| Material | Roughness (rugosidade) | Specular IOR Level | Cor-base (RGB) |
|---|---|---|---|
| MAT_Lambert | 1.0 | 0.05 | (0.75, 0.15, 0.15) |
| MAT_Phong | 0.2 | 0.5 | (0.10, 0.45, 0.80) |
| MAT_BlinnPhong | 0.1 | 0.9 | (0.15, 0.65, 0.30) |

> No Blender 4.5, o input antes chamado "Specular" no Principled BSDF passou a se chamar **Specular IOR Level**. Os valores acima foram ajustados manualmente até a diferença entre os três materiais ficar visível no render de teste, sem estourar as áreas claras nem esconder a forma dos objetos.

## 5. Comparação das aparências observadas

- **MAT_Lambert (Obj_Luminaria):** superfície uniformemente iluminada pela componente difusa, sem ponto de brilho concentrado. A transição entre área iluminada e sombra é suave, e a forma do objeto é lida principalmente pelo gradiente de luz difusa, não por reflexos.
- **MAT_Phong (Obj_Orbe):** além da componente difusa, aparece um highlight especular visível, concentrado numa região menor da superfície, que se desloca conforme o ângulo de observação/câmera. A superfície lê como "polida".
- **MAT_BlinnPhong (Obj_Garra):** comportamento semelhante ao Phong, mas com o highlight mais concentrado e intenso, mesmo com rugosidade ainda mais baixa. A diferença em relação ao Phong fica mais evidente em ângulos rasantes de luz.
- **Influência do ângulo da luz:** ao girar temporariamente `Light_Principal`, o highlight dos materiais Phong e Blinn-Phong se desloca sobre a superfície dos objetos (acompanhando a reflexão especular), enquanto a aparência do material Lambert muda apenas em intensidade geral de iluminação, sem highlight para se mover. Após o teste, a luz foi restaurada à posição descrita na seção 3 para o render final.

## 6. Limitações do Principled BSDF como aproximação

O Principled BSDF do Blender 4.5 é um shader baseado em princípios físicos (physically-based), e seus parâmetros (Roughness, Specular IOR Level etc.) **não implementam literalmente** as equações clássicas de Lambert, Phong ou Blinn-Phong. Nesta atividade, as configurações descritas acima são **aproximações visuais**, escolhidas para tornar perceptível a diferença entre um comportamento puramente difuso (Lambert) e comportamentos com componente especular mais ou menos concentrada (Phong e Blinn-Phong) — não uma implementação matemática exata desses modelos. Uma alternativa mais direta para demonstrar isoladamente a componente difusa de Lambert seria o nó **Diffuse BSDF**, que não possui componente especular.

---
*Imagens relacionadas: render final da cena (`imagem_full.png`) e imagem comparativa dos três objetos/materiais (`Objetos lado a lado.png`) e (`Objetos lado a lado 2.png`).*
