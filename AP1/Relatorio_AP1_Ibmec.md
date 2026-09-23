# Relatório AP1 — Cena-Conceito "Ibmec"
**Aluno(a):** Bernardo de Souza Silva

**Matrícula:** 202108004081

**Curso / Turma:** Engenharia da Computação / Computação Gráfica

**Software:** Blender 4.5 LTS

**Arquivo:** AP1_BernardoSouza.blend

---

## 1. Conceito e título da peça

**Título:** *"Ibmec: Planejando o Futuro e Criando a Inovação"*

**Conceito:** a palavra **Ibmec** é apresentada em três momentos de construção/transformação, cada um protagonizado por um objeto autoral diferente que interage com uma letra específica. A narrativa combina solidez (estrutura da palavra), futuridade (formas geométricas limpas e orbe estilizado) e inovação (elemento mecânico de precisão), reforçando os valores de construção, criatividade e empreendedorismo pedidos no briefing.

## 2. Ideia de entrada, transformação e apresentação da palavra

- **Entrada:** a palavra "Ibmec" começa fragmentada/oculta fora de quadro ou com peças desalinhadas, sugerindo um processo ainda incompleto.
- **Transformação:** três objetos autorais entram em cena, cada um "completando" ou destacando uma letra:
  - a **luminária articulada** desce e ajusta/"acende" o **I**;
  - o **orbe estilizado** se encaixa como ponto do **i**;
  - a **garra mecânica** se fecha formando o **C**.
- **Apresentação:** com os três elementos no lugar, a câmera se aproxima (planejado para AP2) revelando a palavra completa, legível e centralizada — o momento de "marca revelada".

## 3. Identificação dos três objetos autorais e sua função na cena

| Objeto | Descrição de modelagem | Função narrativa/conceitual |
|---|---|---|
| **Luminária articulada** | Base cilíndrica, dois segmentos de braço unidos por "juntas" esféricas, cúpula cônica/tronco de cone. Modelada com primitivas + bevel nas juntas + modificador Subdivision Surface na cúpula. | Representa "trazer luz/inovação" sobre o I; reforça o eixo vertical da peça. |
| **Orbe estilizado** | Icosfera com inset/bevel para criar padrão de facetas ou "anéis" ao redor (toroides extras), sugerindo rede/conexão global. | Ocupa o ponto do "i", simbolizando visão global, tecnologia e conectividade. |
| **Garra mecânica** | Três "dedos" extrudados a partir de um cilindro central, com loop cuts para segmentar as juntas e bevel nas pontas; modificador Mirror para simetria dos dedos. | Fecha-se formando o "C", simbolizando precisão, engenharia e construção. |

> Todos os três objetos são modelagens originais, não referenciando design registrado de terceiros. Eventuais modelos externos usados na cena servem apenas como apoio (ex.: referência de proporção) e não substituem estes três objetos autorais.

## 4. Técnicas de modelagem e transformações utilizadas

- **Modelagem poligonal:** extrusão, inset, loop cut e bevel na construção da luminária e da garra.
- **Curvas/superfícies:** uso de curva Bezier para o braço da luminária (opcional) e/ou Subdivision Surface para suavizar cúpula e orbe.
- **Modificadores:** Subdivision Surface (cúpula/orbe), Mirror (dedos da garra), Bevel (arestas da palavra Ibmec).
- **Transformações geométricas:** translação (posicionamento dos objetos em relação às letras), rotação (ângulo dos dedos da garra, inclinação do braço da luminária), escala (proporção entre a palavra e os objetos, hierarquia visual).
- **Texto:** palavra "Ibmec" criada como texto convertido em malha (Convert to Mesh), com bevel/extrude no próprio objeto de texto para dar volume, mantendo fonte e proporções fiéis à marca.

## 5. Organização da cena no Blender

- Coleção principal: **AP1_Ibmec_Conceito**
  - `Ibmec_Palavra` (malha do texto)
  - `Obj_Luminaria` (base, braço, cúpula agrupados)
  - `Obj_Orbe`
  - `Obj_Garra`
  - `Camera_Principal`
  - `Elementos_Auxiliares` (chão, plano de fundo, etc., se houver)
- Nomes coerentes no Outliner, sem "Cube.001", "Sphere.003" etc.

## 6. Câmera

Câmera principal posicionada em enquadramento frontal/levemente angulado, priorizando a legibilidade da palavra "Ibmec" no centro do quadro. Preparada para receber animação na AP2 (não animada nesta etapa).

## 7. Plano resumido do que será animado e finalizado na AP2

- **Timing:** 15 segundos a 24 fps = 360 frames.
- **Frames 0–90:** entrada dos três objetos autorais e da palavra fragmentada.
- **Frames 90–240:** transformação — luminária ajusta o I, orbe encaixa no ponto do i, garra fecha formando o C; possível movimento de câmera (dolly/zoom).
- **Frames 240–360:** apresentação final da marca completa, câmera estabiliza, iluminação de destaque (a definir na AP2).
- Também serão adicionados na AP2: iluminação (three-point ou HDRI), materiais/texturas (metal escovado na garra e luminária, material translúcido/emissivo no orbe), render engine (Eevee ou Cycles) e exportação do vídeo final.

--- 
*Storyboard referente a este relatório: ver arquivo **[Storyboard_AP1_Ibmec.svg](https://github.com/bernardp112/Computacao_Grafica/blob/main/AP1/Storyboard_AP1_Ibmec.svg)** / imagem anexa.* 
