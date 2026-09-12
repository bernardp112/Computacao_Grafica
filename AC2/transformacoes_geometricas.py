import numpy as np
import matplotlib.pyplot as plt


def configurar_grafico(titulo):
    """Configura os elementos visuais básicos do gráfico."""
    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)
    plt.grid(True)
    plt.axis("equal")
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()


def plot_pontos(original, transformado, titulo):
    """Plota um ponto antes e depois da transformação."""
    plt.figure(figsize=(6, 6))

    plt.scatter(original[0], original[1], label="Original")
    plt.scatter(transformado[0], transformado[1], label="Transformado")

    plt.plot(
        [original[0], transformado[0]],
        [original[1], transformado[1]],
        linestyle="--"
    )

    configurar_grafico(titulo)
    plt.show()


def plot_poligono(original, transformado, titulo):
    """Plota um polígono antes e depois da transformação."""
    plt.figure(figsize=(6, 6))

    original_fechado = np.vstack([original, original[0]])
    transformado_fechado = np.vstack([transformado, transformado[0]])

    plt.plot(
        original_fechado[:, 0],
        original_fechado[:, 1],
        marker="o",
        label="Original"
    )

    plt.plot(
        transformado_fechado[:, 0],
        transformado_fechado[:, 1],
        marker="o",
        linestyle="--",
        label="Transformado"
    )

    configurar_grafico(titulo)
    plt.show()


# ============================================================
# EXERCÍCIO 1 - TRANSLAÇÃO SIMPLES
# ============================================================

P = np.array([2, 3])
vetor = np.array([4, -2])

P1 = P + vetor

print("Exercício 1")
print("P' =", P1)

plot_pontos(
    P,
    P1,
    "Exercício 1 - Translação"
)


# ============================================================
# EXERCÍCIO 2 - ESCALA UNIFORME
# ============================================================

triangulo = np.array([
    [1, 1],
    [3, 1],
    [2, 4]
], dtype=float)

fator = 2

triangulo_escala = triangulo * fator

print("\nExercício 2")
print("Novos vértices:")
print(triangulo_escala)

plot_poligono(
    triangulo,
    triangulo_escala,
    "Exercício 2 - Escala Uniforme"
)


# ============================================================
# EXERCÍCIO 3 - ESCALA NÃO UNIFORME
# ============================================================

fatores = np.array([2, 0.5])

triangulo_nao_uniforme = triangulo * fatores

print("\nExercício 3")
print("Novos vértices:")
print(triangulo_nao_uniforme)

plot_poligono(
    triangulo,
    triangulo_nao_uniforme,
    "Exercício 3 - Escala Não Uniforme"
)


# ============================================================
# EXERCÍCIO 4 - ROTAÇÃO DE 90° ANTI-HORÁRIA
# ============================================================

P = np.array([1, 0], dtype=float)

angulo = np.radians(90)

matriz_rotacao = np.array([
    [np.cos(angulo), -np.sin(angulo)],
    [np.sin(angulo), np.cos(angulo)]
])

P4 = matriz_rotacao @ P
P4 = np.round(P4, 10)

print("\nExercício 4")
print("P' =", P4)

plot_pontos(
    P,
    P4,
    "Exercício 4 - Rotação de 90°"
)


# ============================================================
# EXERCÍCIO 5 - ROTAÇÃO DO QUADRADO
# ============================================================

quadrado = np.array([
    [1, 1],
    [1, 4],
    [4, 4],
    [4, 1]
], dtype=float)

# 45° no sentido horário equivale a -45°
angulo = np.radians(-45)

matriz_rotacao = np.array([
    [np.cos(angulo), -np.sin(angulo)],
    [np.sin(angulo), np.cos(angulo)]
])

quadrado_rotacionado = quadrado @ matriz_rotacao.T

print("\nExercício 5")
print("Novos vértices:")
print(np.round(quadrado_rotacionado, 3))

plot_poligono(
    quadrado,
    quadrado_rotacionado,
    "Exercício 5 - Rotação de 45° Horária"
)


# ============================================================
# EXERCÍCIO 6 - REFLEXÃO NO EIXO Y
# ============================================================

P = np.array([2, 5])

matriz_reflexao_y = np.array([
    [-1, 0],
    [0, 1]
])

P6 = matriz_reflexao_y @ P

print("\nExercício 6")
print("P' =", P6)

plot_pontos(
    P,
    P6,
    "Exercício 6 - Reflexão no Eixo Y"
)


# ============================================================
# EXERCÍCIO 7 - REFLEXÃO DO TRIÂNGULO NO EIXO X
# ============================================================

triangulo7 = np.array([
    [2, 3],
    [4, 3],
    [3, 5]
])

matriz_reflexao_x = np.array([
    [1, 0],
    [0, -1]
])

triangulo_refletido = triangulo7 @ matriz_reflexao_x.T

print("\nExercício 7")
print("Novos vértices:")
print(triangulo_refletido)

plot_poligono(
    triangulo7,
    triangulo_refletido,
    "Exercício 7 - Reflexão no Eixo X"
)


# ============================================================
# EXERCÍCIO 8 - CISALHAMENTO HORIZONTAL
# ============================================================

P = np.array([2, 3])

k = 2

matriz_cisalhamento = np.array([
    [1, k],
    [0, 1]
])

P8 = matriz_cisalhamento @ P

print("\nExercício 8")
print("P' =", P8)

plot_pontos(
    P,
    P8,
    "Exercício 8 - Cisalhamento Horizontal"
)


# ============================================================
# EXERCÍCIO 9 - COMPOSIÇÃO DE TRANSFORMAÇÕES
# ============================================================

P = np.array([3, 2], dtype=float)

# 1. Translação
P_transladado = P + np.array([1, -1])

# 2. Rotação de 90° anti-horária
angulo = np.radians(90)

rotacao90 = np.array([
    [np.cos(angulo), -np.sin(angulo)],
    [np.sin(angulo), np.cos(angulo)]
])

P_rotacionado = rotacao90 @ P_transladado

# 3. Escala uniforme de fator 2
P_final = P_rotacionado * 2

P_rotacionado = np.round(P_rotacionado, 10)
P_final = np.round(P_final, 10)

print("\nExercício 9")
print("Original:", P)
print("Após translação:", P_transladado)
print("Após rotação:", P_rotacionado)
print("Após escala:", P_final)

plt.figure(figsize=(6, 6))

plt.scatter(P[0], P[1], label="Original")
plt.scatter(
    P_transladado[0],
    P_transladado[1],
    label="Após Translação"
)
plt.scatter(
    P_rotacionado[0],
    P_rotacionado[1],
    label="Após Rotação"
)
plt.scatter(
    P_final[0],
    P_final[1],
    label="Após Escala"
)

plt.plot(
    [
        P[0],
        P_transladado[0],
        P_rotacionado[0],
        P_final[0]
    ],
    [
        P[1],
        P_transladado[1],
        P_rotacionado[1],
        P_final[1]
    ],
    linestyle="--"
)

configurar_grafico(
    "Exercício 9 - Composição de Transformações"
)

plt.show()


# ============================================================
# EXERCÍCIO 10 - COMBINAÇÃO DE TRANSFORMAÇÕES
# ============================================================

retangulo = np.array([
    [1, 1],
    [5, 1],
    [5, 3],
    [1, 3]
], dtype=float)

# 1. Translação (-2, 3)
retangulo_transladado = retangulo + np.array([-2, 3])

# 2. Escala não uniforme:
#    1.5 no eixo x e 0.5 no eixo y
retangulo_escalado = retangulo_transladado * np.array([1.5, 0.5])

# 3. Reflexão no eixo y
matriz_reflexao_y = np.array([
    [-1, 0],
    [0, 1]
])

retangulo_final = retangulo_escalado @ matriz_reflexao_y.T

print("\nExercício 10")
print("Original:")
print(retangulo)

print("\nApós translação:")
print(retangulo_transladado)

print("\nApós escala:")
print(retangulo_escalado)

print("\nApós reflexão:")
print(retangulo_final)

plt.figure(figsize=(8, 6))

figuras = [
    (retangulo, "Original"),
    (retangulo_transladado, "Após Translação"),
    (retangulo_escalado, "Após Escala"),
    (retangulo_final, "Após Reflexão")
]

for figura, label in figuras:
    fechada = np.vstack([figura, figura[0]])

    plt.plot(
        fechada[:, 0],
        fechada[:, 1],
        marker="o",
        label=label
    )

configurar_grafico(
    "Exercício 10 - Combinação de Transformações"
)

plt.show()
