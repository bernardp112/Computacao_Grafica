# Relatório AP2 — Peça Final "Ibmec" (15s)

**Aluno(a):** Bernardo de Souza Silva

**Matrícula:** 202108004081

**Disciplina:** Computação Gráfica

**Software:** Blender 4.5 LTS

**Arquivo:** AP2_BernardoSouza.blend

**Vídeo final:** AP2_BernardoSouza.mp4 (15s, 24fps, H.264)

---

## 1. Título, conceito e resumo da sequência

**Título:** *"Construção da Marca"*

**Resumo:** a peça apresenta a marca Ibmec reinterpretando sua própria identidade visual (o "i" com o ponto estilizado) como uma pequena narrativa de construção. Uma luminária reta e branca cai do alto e esmaga a letra "I", que se achata e desaparece — a luminária passa a ocupar o lugar da haste do "i". Em seguida, uma garra mecânica entrega as letras restantes ("b", "m", "e", "c") uma a uma, posicionando-as na frente, até a palavra ficar completa. Por fim, um orbe laranja desce, pousa sobre a cabeça da luminária e acende, funcionando como o ponto do "i" — um farol que marca o fechamento da marca revelada. A paleta de cores (azul-marinho nas letras, laranja no ponto, luminária branca) foi retirada diretamente da identidade visual oficial da Ibmec.

## 2. Momentos/planos e ações animadas

| Momento | Frames | Ação |
|---|---|---|
| 1. Queda | 1 – 49 | A luminária cai de cima em direção à posição do "I" (ainda intacto) |
| 2. Impacto | 50 – 64 | A luminária esmaga o "I" (squash) com um pequeno rebote; a letra achata e desaparece |
| 3. Entrega | 90 – 320 | A garra pega, carrega e posiciona "b" (90–145), "m" (150–205), "e" (210–265) e "c" (270–320), uma de cada vez, fechando os dedos ao pegar e abrindo bem ao soltar |
| 4. Encerramento | 320 – 360 | O orbe desce, se acomoda sobre a luminária e acende como um farol (emissão + luz puntual) |

## 3. Propriedades animadas e decisões de timing/interpolação

- **Luminária (`Obj_Luminaria`):** `location` e `scale` — cai de uma posição elevada (frame 1) até a posição final no frame 50, com um squash (achatamento) no instante do impacto e um pequeno rebote até o frame 70.
- **Letra "I" (`Letra_I`):** `scale` — permanece visível e parada do frame 1 ao 49; achata no frame 50 (mesmo instante do impacto da luminária) e desaparece (escala ≈0) a partir do frame 64.
- **Letras "b", "m", "e", "c":** `location` — cada uma entra deslocada e chega à posição final dentro da sua janela de entrega (ver tabela acima).
- **Garra (`Obj_Garra`) e seus 3 dedos:** `location` (corpo) e `rotation_euler` (dedos) — o corpo se desloca até o ponto de pega de cada letra; os dedos fecham (0°) exatamente no instante da pega e permanecem fechados durante o transporte; abrem bem largo (60°) pouco depois de soltar cada letra, antes de seguir para a próxima.
- **Orbe (`Obj_Orbe`):** `location` — desce de uma posição deslocada até pousar sobre a cabeça da luminária, com uma folga fixa e uniforme acima dela; `Emission Strength` do material (e `energy` de uma luz puntual filha) sobem de 0 a um valor alto logo após o pouso, criando o efeito de farol aceso.
- **Câmera (`Camera_Principal`):** `location` e `lens` — leve aproximação (zoom-in) ao longo de toda a peça, com a Profundidade de Campo (DOF) mantendo a palavra em foco e o fundo discretamente desfocado.
- Todas as transições usam a interpolação padrão do Blender (Bezier), suavizando entradas e saídas de cada movimento.

## 4. Configuração de iluminação e renderização

- **Iluminação de cena:** `Light_Principal` (Area, em ângulo, para gerar sombras e realces perceptíveis) + `Light_Preenchimento` (Sun, baixa intensidade, para suavizar sombras). Uma luz puntual adicional (`Light_Farol_Orbe`), filha do orbe, acende apenas no encerramento para reforçar o efeito de farol.
- **Cenário/profundidade:** um chão fosco escuro e uma parede de fundo com gradiente vertical (mais escura embaixo, mais clara em cima) dão profundidade à composição, evitando o fundo vazio. A Profundidade de Campo da câmera desfoca sutilmente esse fundo, destacando a palavra.
- **Motor de render:** Eevee (Blender 4.5 LTS).
- **Resolução:** 1920×1080, 24 fps, frames 1–360 (15 segundos).
- **Saída:** vídeo .mp4, codec H.264 (FFmpeg).
- O Principled BSDF usado em todos os materiais é um shader baseado em princípios físicos (PBR); suas propriedades (Roughness, Metallic, Emission) são aproximações visuais, não implementações literais dos modelos clássicos estudados na AC04.

## 5. Materiais e cores

| Objeto | Material | Cor | Observação |
|---|---|---|---|
| Letras (I, b, m, e, c) | `MAT_Ibmec_Marca` | Azul-marinho | Cor extraída da identidade visual oficial da Ibmec |
| `Obj_Luminaria` | `MAT_Luminaria_Branca` | Branco | Metallic 0, Roughness moderado (acabamento fosco) |
| `Obj_Garra` + dedos | `MAT_Metal_Escovado` | Cinza metálico | Metallic 1.0, Roughness baixo |
| `Obj_Orbe` | `MAT_Orbe_Laranja` | Laranja/dourado | Cor extraída do ponto da marca Ibmec; ganha Emission no encerramento para o efeito de farol |

> Nesta versão final, os materiais foram simplificados para cores sólidas PBR (sem texturas de imagem), priorizando a reconstrução confiável da cena do zero. Se desejar reaplicar as texturas de imagem (madeira/metal escovado) desenvolvidas na AC05, isso pode ser feito por cima desta cena, reatribuindo-as aos objetos autorais.

## 6. Desafios encontrados e soluções adotadas

- **Orientação das letras:** os objetos de texto nascem "deitados" no plano XY; foi necessário rotacionar 90° em X e aplicar (bake) essa rotação para que as letras ficassem de pé, de frente para a câmera.
- **Espaçamento e alinhamento das letras:** o espaçamento inicial entre letras ficou colado demais (corrigido aumentando o `gap`); o alinhamento vertical ("align_y") inicialmente gerava letras em alturas de linha de base diferentes — resolvido recalculando a base de cada letra pela caixa delimitadora real e forçando-a para o nível do chão (z=0).
- **Sobreposição luminária/letra "I":** a base cilíndrica da luminária inicialmente colidia com toda a extensão da letra "I". A solução final foi redesenhar a luminária como um poste reto (em vez do formato articulado inicial) e permitir a sobreposição breve apenas no instante do esmagamento, já que a letra desaparece logo em seguida.
- **Escala e nível da luminária:** depois de reduzir seu tamanho para não ficar mais alta que as letras, foi preciso recalcular a origem do objeto pela caixa delimitadora para garantir que a base continuasse exatamente no nível do chão.
- **Garra "simples demais":** o desenho inicial (um cilindro com três dedos retos) foi substituído por um corpo cônico, um anel decorativo, um braço longo (saindo do quadro) e dedos afunilados com uma junta — resultando em um visual mais elaborado.
- **Dedos abrindo/fechando:** os três dedos precisaram virar objetos independentes (filhos do corpo da garra, com a origem no ponto de encaixe) para poder animar a abertura e o fechamento como uma garra real; o sentido de rotação (sinal do ângulo) precisou ser invertido após o primeiro teste, pois os dedos fechavam quando deveriam abrir.
- **Origem do corpo da garra após alongar o braço:** ao juntar as peças do corpo em um único objeto, o Blender herdou a origem do braço (agora muito longo), fazendo `claw.location` apontar para o meio do braço em vez do ponto de pega — corrigido recolocando a origem no ponto de encaixe dos dedos.
- **Distância do orbe até a luminária:** o deslocamento fixo usado inicialmente ficou desatualizado após redimensionar a luminária; a solução foi calcular a posição do orbe dinamicamente a partir do topo real da luminária (via caixa delimitadora), com uma folga configurável.

## 7. Fontes e licenças de recursos externos

- Nenhum modelo 3D ou textura de imagem externa foi utilizado nesta versão final — todos os objetos (letras, luminária, orbe, garra, cenário) foram modelados inteiramente via script no Blender, a partir de primitivas.
- A paleta de cores (azul-marinho, laranja, branco) foi definida com base na identidade visual oficial da Ibmec, fornecida pelo próprio aluno como referência.
- Nenhum áudio foi utilizado nesta entrega.

---
*Arquivos relacionados: `AP2_BernardoSouza.blend`, `AP2_BernardoSouza.mp4`, imagem do quadro final renderizado, `Storyboard_AP2_Ibmec_FINAL.svg`.*
