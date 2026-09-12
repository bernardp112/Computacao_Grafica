# Atividade — Transformações Geométricas com Matplotlib

## Exercício 1 — Translação Simples

Dado o ponto:

\[
P(2,3)
\]

Aplicando a translação com vetor:

\[
(4,-2)
\]

Temos:

\[
P' = (2+4,\ 3-2)
\]

\[
\boxed{P'(6,1)}
\]

As duas coordenadas foram alteradas:
- \(x: 2 \rightarrow 6\)
- \(y: 3 \rightarrow 1\)

---

## Exercício 2 — Escala Uniforme

Triângulo original:

- \(A(1,1)\)
- \(B(3,1)\)
- \(C(2,4)\)

Aplicando escala uniforme de fator 2:

\[
x' = 2x
\]

\[
y' = 2y
\]

Novos vértices:

- \(A'(2,2)\)
- \(B'(6,2)\)
- \(C'(4,8)\)

Portanto:

\[
\boxed{A'(2,2),\ B'(6,2),\ C'(4,8)}
\]

O triângulo mantém sua forma e seus ângulos, mas suas dimensões lineares dobram. Como a escala é aplicada nos dois eixos, sua área se torna 4 vezes maior.

---

## Exercício 3 — Escala Não Uniforme

Usando o mesmo triângulo:

- \(A(1,1)\)
- \(B(3,1)\)
- \(C(2,4)\)

Aplicando:

- fator 2 no eixo \(x\)
- fator 0,5 no eixo \(y\)

Temos:

\[
x' = 2x
\]

\[
y' = 0,5y
\]

Novos vértices:

- \(A'(2,0.5)\)
- \(B'(6,0.5)\)
- \(C'(4,2)\)

Portanto:

\[
\boxed{A'(2,0.5),\ B'(6,0.5),\ C'(4,2)}
\]

---

## Exercício 4 — Rotação em Torno da Origem

Ponto original:

\[
P(1,0)
\]

Uma rotação de 90° no sentido anti-horário transforma:

\[
(x,y) \rightarrow (-y,x)
\]

Logo:

\[
(1,0) \rightarrow (0,1)
\]

Portanto:

\[
\boxed{P'(0,1)}
\]

---

## Exercício 5 — Rotação de um Polígono

Quadrado original:

- \(A(1,1)\)
- \(B(1,4)\)
- \(C(4,4)\)
- \(D(4,1)\)

A rotação de 45° no sentido horário corresponde a um ângulo de \(-45^\circ\).

A matriz utilizada é:

\[
R(\theta)=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
\]

Para \(\theta=-45^\circ\), os novos vértices são aproximadamente:

- \(A'(1.414,0)\)
- \(B'(3.536,2.121)\)
- \(C'(5.657,0)\)
- \(D'(3.536,-2.121)\)

Portanto:

\[
\boxed{
A'(1.414,0),\
B'(3.536,2.121),\
C'(5.657,0),\
D'(3.536,-2.121)
}
\]

---

## Exercício 6 — Reflexão Simples

Ponto original:

\[
P(2,5)
\]

Na reflexão em relação ao eixo \(y\):

\[
(x,y) \rightarrow (-x,y)
\]

Logo:

\[
(2,5) \rightarrow (-2,5)
\]

Portanto:

\[
\boxed{P'(-2,5)}
\]

---

## Exercício 7 — Reflexão de um Triângulo

Triângulo original:

- \(A(2,3)\)
- \(B(4,3)\)
- \(C(3,5)\)

Na reflexão em relação ao eixo \(x\):

\[
(x,y) \rightarrow (x,-y)
\]

Assim:

- \(A'(2,-3)\)
- \(B'(4,-3)\)
- \(C'(3,-5)\)

Portanto:

\[
\boxed{A'(2,-3),\ B'(4,-3),\ C'(3,-5)}
\]

---

## Exercício 8 — Cisalhamento Horizontal

Ponto original:

\[
P(2,3)
\]

Para um cisalhamento horizontal com \(k=2\):

\[
x' = x + ky
\]

\[
y' = y
\]

Substituindo:

\[
x' = 2 + 2(3) = 8
\]

\[
y' = 3
\]

Portanto:

\[
\boxed{P'(8,3)}
\]

---

## Exercício 9 — Composição de Transformações

Ponto inicial:

\[
P(3,2)
\]

### 1. Translação com vetor \((1,-1)\)

\[
(3,2)+(1,-1)=(4,1)
\]

### 2. Rotação de 90° no sentido anti-horário

\[
(x,y)\rightarrow(-y,x)
\]

\[
(4,1)\rightarrow(-1,4)
\]

### 3. Escala uniforme com fator 2

\[
(-1,4)\rightarrow(-2,8)
\]

Resultado final:

\[
\boxed{P'(-2,8)}
\]

---

## Exercício 10 — Combinação de Transformações em uma Figura

Retângulo original:

- \(A(1,1)\)
- \(B(5,1)\)
- \(C(5,3)\)
- \(D(1,3)\)

### 1. Translação com vetor \((-2,3)\)

- \(A\rightarrow(-1,4)\)
- \(B\rightarrow(3,4)\)
- \(C\rightarrow(3,6)\)
- \(D\rightarrow(-1,6)\)

### 2. Escala não uniforme

Fatores:

- \(1.5\) no eixo \(x\)
- \(0.5\) no eixo \(y\)

Resultados:

- \(A\rightarrow(-1.5,2)\)
- \(B\rightarrow(4.5,2)\)
- \(C\rightarrow(4.5,3)\)
- \(D\rightarrow(-1.5,3)\)

### 3. Reflexão em relação ao eixo \(y\)

Na reflexão:

\[
(x,y)\rightarrow(-x,y)
\]

Resultados finais:

- \(A'(1.5,2)\)
- \(B'(-4.5,2)\)
- \(C'(-4.5,3)\)
- \(D'(1.5,3)\)

Portanto:

\[
\boxed{
A'(1.5,2),\
B'(-4.5,2),\
C'(-4.5,3),\
D'(1.5,3)
}
\]

---

# Matrizes utilizadas

## Rotação

\[
R(\theta)=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
\]

## Reflexão no eixo \(x\)

\[
R_x=
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
\]

## Reflexão no eixo \(y\)

\[
R_y=
\begin{bmatrix}
-1 & 0 \\
0 & 1
\end{bmatrix}
\]

## Cisalhamento horizontal

\[
H=
\begin{bmatrix}
1 & k \\
0 & 1
\end{bmatrix}
\]

No cisalhamento horizontal:

\[
x'=x+ky
\]

\[
y'=y
\]

---

## Observação

A ordem das transformações é importante. Em exercícios com composição, como os exercícios 9 e 10, alterar a ordem de translação, rotação, escala ou reflexão pode produzir um resultado final diferente.
