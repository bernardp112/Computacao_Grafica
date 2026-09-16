##1. Diferença entre translação, rotação e escala
Translação altera a posição de um objeto no espaço, sem modificar sua orientação ou tamanho.

Rotação altera a orientação do objeto em torno de um determinado eixo.

Escala altera o tamanho do objeto, podendo ser uniforme ou diferente em cada eixo.

Por exemplo, mover um cubo de (0,0,0) para (2,0,0) é uma translação; girá-lo 45° no eixo Z é uma rotação; e aumentar seu tamanho de (1,1,1) para (2,2,2) é uma escala.

##2. Espaço local × espaço global
O espaço global utiliza os eixos fixos da cena, independentemente da orientação do objeto.

O espaço local utiliza os próprios eixos do objeto, que podem ter sido modificados por rotações anteriores.

Isso significa que, depois de girar um objeto, movimentá-lo no eixo X local pode produzir uma direção diferente daquela obtida movimentando-o no X global.

##3. Por que rotações em eixos diferentes produzem resultados distintos?
Porque cada eixo representa uma direção diferente no espaço 3D. Além disso, rotações sucessivas podem alterar a orientação dos eixos locais do objeto.

Por isso, aplicar 45° em X e depois 45° em Y não produz necessariamente o mesmo resultado que aplicar as rotações em outra ordem.

##4. Por que usar math.radians()?
O Blender utiliza radianos para representar os valores de rotation_euler no Python.

Como normalmente pensamos em ângulos em graus, math.radians() permite converter, por exemplo:
´´´
math.radians(90)
´´´
para o valor correspondente em radianos.

Assim, podemos escrever o código de maneira mais intuitiva usando graus.

##5. Quando Python é melhor que a transformação manual?
Python é especialmente útil quando precisamos criar ou transformar muitos objetos de maneira repetitiva e precisa.

Por exemplo, em vez de criar manualmente 50 cubos e posicionar cada um individualmente, podemos utilizar um script para criar todos eles automaticamente, definindo suas posições, rotações e escalas.
