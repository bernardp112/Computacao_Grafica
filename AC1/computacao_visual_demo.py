"""
Demonstração das áreas de Computação Visual:
1. Síntese de Imagens / Computação Gráfica
2. Processamento de Imagens
3. Visão Computacional
4. Visualização Computacional

Dependências:
pip install numpy matplotlib pillow opencv-python scikit-image
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import cv2
from skimage import data

OUT = "resultados_computacao_visual"
os.makedirs(OUT, exist_ok=True)

# =========================================================
# 1) SÍNTESE DE IMAGENS / COMPUTAÇÃO GRÁFICA
# =========================================================
# A imagem não existe previamente: ela é criada a partir de
# primitivas geométricas, coordenadas, cores e uma ordem de desenho.

W, H = 900, 520
img = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(img)

for y in range(H):
    t = y / H
    draw.line(
        [(0, y), (W, y)],
        fill=(int(120 + 100*t), int(190 + 45*t), int(245 - 40*t))
    )

draw.ellipse((690, 55, 800, 165), fill=(255, 220, 90))
draw.polygon([(0, 360), (190, 150), (360, 360)], fill=(95, 120, 140))
draw.polygon([(210, 360), (465, 115), (720, 360)], fill=(75, 100, 125))
draw.polygon([(525, 360), (720, 180), (900, 360)], fill=(105, 125, 145))
draw.rectangle((0, 360, W, H), fill=(72, 145, 78))
draw.rectangle((110, 315, 290, 440), fill=(224, 175, 110), outline=(70, 50, 40), width=3)
draw.polygon([(90, 315), (200, 235), (310, 315)], fill=(145, 65, 45), outline=(70, 50, 40))
draw.rectangle((180, 365, 225, 440), fill=(110, 75, 55))
draw.rectangle((710, 335, 735, 455), fill=(100, 65, 40))

for box in [(655,260,790,390), (675,220,770,340), (692,185,752,300)]:
    draw.ellipse(box, fill=(45, 120, 60))

img.save(os.path.join(OUT, "01_sintese.png"))

# =========================================================
# 2) PROCESSAMENTO DE IMAGENS
# =========================================================
# Entrada: imagem pronta.
# Saída: outra representação da mesma imagem após operações
# sobre os pixels.

rgb = data.astronaut()
bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 1.2)
edges = cv2.Canny(blur, 70, 150)

fig, ax = plt.subplots(1, 3, figsize=(12, 4))
ax[0].imshow(rgb); ax[0].set_title("Original"); ax[0].axis("off")
ax[1].imshow(blur, cmap="gray"); ax[1].set_title("GaussianBlur"); ax[1].axis("off")
ax[2].imshow(edges, cmap="gray"); ax[2].set_title("Canny"); ax[2].axis("off")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "02_processamento.png"), dpi=170)
plt.close()

# =========================================================
# 3) VISÃO COMPUTACIONAL
# =========================================================
# Aqui não queremos somente alterar pixels, mas interpretar
# o conteúdo da cena: localizar uma face.

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(40, 40)
)

detected = rgb.copy()
for (x, y, w, h) in faces:
    cv2.rectangle(detected, (x, y), (x+w, y+h), (255, 0, 0), 3)

plt.figure(figsize=(7, 6))
plt.imshow(detected)
plt.title(f"Faces detectadas: {len(faces)}")
plt.axis("off")
plt.savefig(os.path.join(OUT, "03_visao_computacional.png"), dpi=170, bbox_inches="tight")
plt.close()

print("Faces detectadas:", len(faces))

# =========================================================
# 4) VISUALIZAÇÃO COMPUTACIONAL
# =========================================================
# O objetivo é converter dados abstratos/numericos em uma
# representação visual que facilite a análise.

x = np.linspace(-8, 8, 220)
y = np.linspace(-8, 8, 220)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Z = np.sinc(R / np.pi)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X, Y, Z, cmap="viridis", linewidth=0)
ax.set_title("Campo escalar z = sin(r)/r")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.colorbar(surf, shrink=0.65, label="valor de z")
plt.savefig(os.path.join(OUT, "04_visualizacao.png"), dpi=170, bbox_inches="tight")
plt.close()
