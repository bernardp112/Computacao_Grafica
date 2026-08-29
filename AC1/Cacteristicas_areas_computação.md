# Computação Visual: diferenças entre Síntese de Imagens, Processamento de Imagens, Visão Computacional e Visualização Computacional

## 1. Introdução

Computação Visual é uma área ampla da Computação que envolve técnicas de geração, manipulação, interpretação e representação de informações visuais. Apesar de áreas como Computação Gráfica, Processamento de Imagens, Visão Computacional e Visualização Computacional trabalharem diretamente com imagens, seus objetivos são diferentes.

De maneira simplificada, é possível distinguir as quatro áreas da seguinte forma:

| Área                                        | Entrada                                   | Objetivo principal                      | Saída                   |
| ------------------------------------------- | ----------------------------------------- | --------------------------------------- | ----------------------- |
| **Síntese de Imagens / Computação Gráfica** | Modelos, formas, coordenadas e parâmetros | Gerar uma imagem artificial             | Imagem                  |
| **Processamento de Imagens**                | Imagem existente                          | Modificar ou melhorar seus pixels       | Imagem modificada       |
| **Visão Computacional**                     | Imagem ou vídeo                           | Interpretar e compreender o conteúdo    | Informação/conhecimento |
| **Visualização Computacional**              | Dados numéricos ou abstratos              | Tornar dados compreensíveis visualmente | Representação gráfica   |

Uma forma ainda mais simples de compreender as diferenças é:

**Computação Gráfica:** dados → imagem.

**Processamento de Imagens:** imagem → imagem.

**Visão Computacional:** imagem → informação.

**Visualização Computacional:** dados → representação visual para análise.

---

# 2. Síntese de Imagens — Computação Gráfica

## 2.1 Características

A Síntese de Imagens, normalmente associada à Computação Gráfica, é responsável pela criação artificial de imagens utilizando modelos matemáticos e computacionais.

Diferentemente do Processamento de Imagens, não é necessário possuir uma fotografia previamente existente. A imagem pode ser inteiramente produzida pelo computador.

Entre os principais elementos dessa área estão:

* primitivas geométricas;
* coordenadas;
* transformações;
* cores;
* texturas;
* iluminação;
* câmeras virtuais;
* rasterização;
* ray tracing;
* modelagem 2D e 3D.

Computação Gráfica é utilizada, por exemplo, em jogos digitais, animações, filmes, simuladores, arquitetura, CAD e realidade virtual.

Um exemplo bastante conhecido de projeto público relacionado à síntese de imagens é o **[Ray Tracing in One Weekend](https://github.com/RayTracing/raytracing.github.io)**, que apresenta a construção de um renderizador baseado em ray tracing. Seu repositório disponibiliza gratuitamente os códigos-fonte dos renderizadores utilizados nos livros.

Outro exemplo de biblioteca pública relacionada à síntese e manipulação de imagens é a **[Pillow](https://github.com/python-pillow/Pillow/)**, uma biblioteca open-source para Python que permite criar e editar imagens por meio de operações como desenho de formas geométricas, aplicação de cores, textos, filtros e transformações. A biblioteca é uma evolução da Python Imaging Library (PIL) e possui código-fonte e documentação disponíveis publicamente, sendo adequada para demonstrar conceitos básicos de geração e rasterização de imagens em duas dimensões.

### Aplicação escolhida

**Geração de uma cena sintética utilizando primitivas gráficas.**

Foi criada uma pequena paisagem utilizando formas geométricas como:

* retângulos;
* círculos;
* elipses;
* polígonos;
* linhas;
* gradientes.

O princípio é semelhante ao processo de rasterização utilizado em sistemas gráficos: objetos matematicamente definidos são transformados em pixels.

### Código principal

```python
from PIL import Image, ImageDraw

W, H = 900, 520

img = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(img)

# Céu em gradiente
for y in range(H):
    t = y / H

    draw.line(
        [(0, y), (W, y)],
        fill=(
            int(120 + 100*t),
            int(190 + 45*t),
            int(245 - 40*t)
        )
    )

# Sol
draw.ellipse(
    (690, 55, 800, 165),
    fill=(255, 220, 90)
)

# Montanhas
draw.polygon(
    [(0, 360), (190, 150), (360, 360)],
    fill=(95, 120, 140)
)

draw.polygon(
    [(210, 360), (465, 115), (720, 360)],
    fill=(75, 100, 125)
)

# Solo
draw.rectangle(
    (0, 360, W, H),
    fill=(72, 145, 78)
)

# Casa
draw.rectangle(
    (110, 315, 290, 440),
    fill=(224, 175, 110)
)

draw.polygon(
    [(90, 315), (200, 235), (310, 315)],
    fill=(145, 65, 45)
)

img.save("01_sintese.png")
```

## 2.2 Aspectos específicos da área

Um aspecto importante deste exemplo é que **não existe uma imagem original sendo alterada**.

O computador recebe apenas especificações como:

```text
posição
tamanho
forma
cor
ordem de desenho
```

Por exemplo:

```python
draw.ellipse((690, 55, 800, 165))
```

define matematicamente a região na qual o sol deve ser rasterizado.

Já:

```python
draw.polygon(
    [(0, 360), (190, 150), (360, 360)]
)
```

define os vértices de um polígono que posteriormente é transformado em pixels.

Portanto, o fluxo dessa área é:

**Descrição matemática da cena → renderização → imagem**

### Resultado executado

[Ver resultado da Síntese de Imagens](https://github.com/bernardp112/Computacao_Grafica/blob/main/AC1/01_sintese_computacao_grafica.png)

---

# 3. Processamento de Imagens

## 3.1 Características

Processamento de Imagens envolve operações realizadas sobre uma imagem já existente.

Seu principal objetivo normalmente não é entender semanticamente o conteúdo da imagem, mas modificar sua representação.

Entre suas aplicações estão:

* remoção de ruído;
* aumento de contraste;
* correção de brilho;
* filtragem;
* suavização;
* detecção de bordas;
* segmentação baseada em pixels;
* transformações geométricas;
* compressão.

Para esta demonstração foi utilizado o **[OpenCV](https://github.com/opencv/opencv)**, um projeto open-source voltado para processamento de imagens e visão computacional. Seu repositório possui módulos relacionados explicitamente a processamento de imagens e computer vision.

### Aplicação escolhida

**Suavização da imagem e detecção de bordas utilizando Gaussian Blur e algoritmo de Canny.**

Foram realizadas três etapas:

```text
Imagem original
       ↓
Conversão para tons de cinza
       ↓
Filtro Gaussiano
       ↓
Detector de bordas Canny
```

### Código

```python
import cv2
from skimage import data

imagem = data.astronaut()

imagem_bgr = cv2.cvtColor(
    imagem,
    cv2.COLOR_RGB2BGR
)

cinza = cv2.cvtColor(
    imagem_bgr,
    cv2.COLOR_BGR2GRAY
)

suavizada = cv2.GaussianBlur(
    cinza,
    (5, 5),
    1.2
)

bordas = cv2.Canny(
    suavizada,
    70,
    150
)
```

## 3.2 Filtro Gaussiano

A operação:

```python
cv2.GaussianBlur(cinza, (5, 5), 1.2)
```

aplica uma suavização na imagem.

Ela utiliza uma distribuição Gaussiana para calcular novos valores para os pixels considerando seus vizinhos.

O objetivo é reduzir pequenas variações e ruídos.

O parâmetro:

```python
(5, 5)
```

representa o tamanho do kernel utilizado durante a convolução.

De maneira simplificada, cada pixel deixa de depender somente de seu valor original e passa a considerar os pixels ao seu redor.

---

## 3.3 Detector de bordas Canny

Posteriormente é utilizada a função:

```python
cv2.Canny(suavizada, 70, 150)
```

O algoritmo de Canny procura regiões nas quais ocorre uma mudança significativa de intensidade.

Essas regiões normalmente correspondem a limites de objetos.

Os valores:

```text
70
150
```

funcionam como limiares utilizados na identificação das bordas.

O resultado deixa evidente uma característica fundamental do Processamento de Imagens:

**uma imagem foi recebida e outra imagem foi produzida.**

Nenhuma tentativa explícita foi feita de identificar que existe uma pessoa na imagem.

Portanto:

**Imagem → transformação matemática → nova imagem**

### Resultado executado

[Ver resultado do Processamento de Imagens](https://github.com/bernardp112/Computacao_Grafica/blob/main/AC1/02_processamento_imagens.png)

---

# 4. Visão Computacional ou Visão Artificial

## 4.1 Características

Visão Computacional busca permitir que sistemas computacionais obtenham informações sobre o conteúdo de imagens e vídeos.

Enquanto Processamento de Imagens concentra-se principalmente em modificar os pixels, Visão Computacional procura responder perguntas como:

* Existe uma pessoa na imagem?
* Onde está seu rosto?
* Qual objeto aparece na fotografia?
* Quantas pessoas existem?
* Que movimento está acontecendo?
* Qual é a placa de um veículo?
* A imagem possui algum defeito?

Entre as principais aplicações estão:

* reconhecimento facial;
* reconhecimento de objetos;
* classificação de imagens;
* reconhecimento de caracteres;
* veículos autônomos;
* inspeção industrial;
* rastreamento de objetos;
* diagnóstico auxiliado por imagens;
* sistemas de segurança.

### Aplicação escolhida

**Detecção automática de faces utilizando Haar Cascade do OpenCV.**

O próprio projeto [OpenCV](https://github.com/opencv/opencv) possui classificadores Haar e exemplos de detecção facial utilizando arquivos de cascade fornecidos com o projeto.

### Código

```python
import cv2

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades
    + "haarcascade_frontalface_default.xml"
)

faces = cascade.detectMultiScale(
    cinza,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(40, 40)
)

for (x, y, w, h) in faces:

    cv2.rectangle(
        imagem,
        (x, y),
        (x + w, y + h),
        (255, 0, 0),
        3
    )
```

## 4.2 Haar Cascade

O classificador Haar procura padrões visuais característicos utilizando características semelhantes a regiões claras e escuras.

O sistema percorre diferentes regiões e escalas da imagem procurando combinações compatíveis com uma face.

A função:

```python
detectMultiScale()
```

retorna as coordenadas dos objetos encontrados:

```text
x
y
largura
altura
```

Representadas por:

```python
(x, y, w, h)
```

Essas coordenadas permitem localizar a face na imagem.

Na execução realizada para este trabalho o algoritmo encontrou:

**1 face.**

Este detalhe mostra a principal diferença em relação ao Processamento de Imagens.

No exemplo anterior, a resposta do programa era uma nova matriz de pixels contendo bordas.

Neste exemplo, o sistema produz uma informação:

> Há uma face e ela se encontra em determinada posição da imagem.

Portanto:

**Imagem → análise → informação sobre a cena**

### Resultado executado

[Ver resultado da Visão Computacional](https://github.com/bernardp112/Computacao_Grafica/blob/main/AC1/03_visao_computacional_face.png)

---

# 5. Visualização Computacional

## 5.1 Características

Visualização Computacional utiliza recursos gráficos para transformar dados em representações visuais que sejam mais fáceis de analisar.

Nesse caso, o objetivo não é necessariamente criar uma cena realista e nem interpretar uma fotografia.

A finalidade é facilitar a compreensão de dados.

Algumas aplicações são:

* gráficos científicos;
* visualização de dados estatísticos;
* mapas;
* visualizações tridimensionais;
* visualização médica;
* visualização de simulações;
* análise financeira;
* dashboards;
* visualização de grandes conjuntos de dados.

Para este exemplo foi utilizado **[Matplotlib](https://github.com/matplotlib/matplotlib)**, biblioteca open-source criada especificamente para geração de visualizações estáticas, animadas e interativas em Python.

O projeto também disponibiliza uma extensa galeria pública contendo exemplos e códigos de diferentes formas de visualização.

### Aplicação escolhida

**Visualização tridimensional de um campo escalar.**

Foi utilizada a função:

$$
z = \frac{\sin(r)}{r}
$$

em que:

$$
r=\sqrt{x^2+y^2}
$$

Esse conjunto de valores numéricos foi convertido em uma superfície tridimensional.

### Código

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-8, 8, 220)
y = np.linspace(-8, 8, 220)

X, Y = np.meshgrid(x, y)

R = np.sqrt(
    X**2 + Y**2
)

Z = np.sinc(
    R / np.pi
)

fig = plt.figure()

ax = fig.add_subplot(
    111,
    projection="3d"
)

surface = ax.plot_surface(
    X,
    Y,
    Z,
    cmap="viridis"
)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.show()
```

## 5.2 Aspectos específicos

Inicialmente não existe nenhuma imagem.

Existem apenas conjuntos de valores:

```python
X
Y
Z
```

A função:

```python
plot_surface()
```

transforma essas informações em uma superfície tridimensional.

Neste caso, a cor também representa numericamente diferentes valores da função.

O fluxo é:

**Dados numéricos → mapeamento visual → visualização**

Embora isso possa parecer semelhante à Computação Gráfica, existe uma diferença importante.

Na Computação Gráfica, normalmente a preocupação principal é construir uma cena ou imagem.

Na Visualização Computacional, a imagem é principalmente um **instrumento para compreender dados**.

### Resultado executado

[Ver resultado da Visualização Computacional](https://github.com/bernardp112/Computacao_Grafica/blob/main/AC1/04_visualizacao_computacional.png)

---

# 6. Comparação das quatro aplicações

Os quatro experimentos realizados podem ser resumidos da seguinte maneira:

| Área                       | Exemplo executado     | Entrada                         | Operação                  | Resultado         |
| -------------------------- | --------------------- | ------------------------------- | ------------------------- | ----------------- |
| Computação Gráfica         | Criação de paisagem   | Coordenadas, cores e primitivas | Rasterização              | Nova imagem       |
| Processamento de Imagens   | Canny + Gaussian Blur | Fotografia                      | Operações sobre pixels    | Imagem de bordas  |
| Visão Computacional        | Detecção de face      | Fotografia                      | Classificação/localização | Face identificada |
| Visualização Computacional | Superfície 3D         | Valores de uma função           | Mapeamento visual         | Gráfico 3D        |

Existe especialmente uma diferença interessante entre Processamento de Imagens e Visão Computacional.

No processamento:

```text
Foto
 ↓
Filtro
 ↓
Imagem com bordas
```

Na visão computacional:

```text
Foto
 ↓
Algoritmo de detecção
 ↓
"Existe uma face nesta posição"
```

Já a Computação Gráfica executa praticamente o caminho inverso:

```text
Modelo matemático
 ↓
Renderização
 ↓
Imagem
```

E a Visualização Computacional transforma informações abstratas em algo visual:

```text
Dados
 ↓
Mapeamento visual
 ↓
Gráfico ou representação
 ↓
Interpretação humana
```

---

# 7. Relação entre as áreas

Apesar das diferenças, as quatro áreas frequentemente trabalham juntas.

Um veículo autônomo, por exemplo, poderia utilizar:

**Visão Computacional** para identificar pedestres e veículos.

**Processamento de Imagens** para reduzir ruído das câmeras e melhorar a qualidade das imagens.

**Computação Gráfica** para gerar um ambiente de simulação utilizado no treinamento do sistema.

**Visualização Computacional** para apresentar aos engenheiros informações provenientes dos sensores, trajetórias e decisões realizadas pelo sistema.

Outro exemplo são aplicações médicas. Uma tomografia pode passar por processamento para remoção de ruídos, Visão Computacional para identificação automática de possíveis anomalias e Visualização Computacional para apresentar estruturas tridimensionais para médicos.

---

# 8. Conclusão

As áreas relacionadas à Computação Visual possuem técnicas semelhantes em alguns aspectos, porém apresentam objetivos diferentes. A **Síntese de Imagens ou Computação Gráfica** concentra-se na criação de imagens a partir de descrições matemáticas e computacionais. O **Processamento de Imagens** parte de uma imagem existente e realiza alterações em seus pixels para melhorar, transformar ou destacar determinadas características.

A **Visão Computacional**, por sua vez, procura interpretar o conteúdo visual e extrair conhecimento, como demonstrado pela identificação automática de uma face. Já a **Visualização Computacional** utiliza elementos gráficos para representar informações abstratas ou numéricas, permitindo que seres humanos identifiquem padrões e compreendam fenômenos complexos com maior facilidade. Os experimentos demonstram, portanto, que embora todas as áreas trabalhem com informação visual, existe uma diferença fundamental entre **produzir imagens, transformar imagens, compreender imagens e utilizar imagens para compreender dados**.
