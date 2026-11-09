import cv2, numpy as np, random, glob

random.seed(42)  # semilla fija: muestra reproducible
rutas = random.sample(sorted(glob.glob("imgs/*.png")), 100)

for r in rutas:
    bgr = cv2.imread(r, cv2.IMREAD_COLOR)
    if bgr is None:
        print(f"No se pudo leer {r}")
        continue
    # Misma conversión a grises que el notebook (Y = 0.299 R + 0.587 G + 0.114 B)
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    media, std = g.mean(), g.std()
    sat = (g >= 250).mean() * 100  # % de píxeles casi saturados
    # Ruido: desviación típica del residuo respecto a la mediana 3×3
    ruido = np.std(g.astype(float) - cv2.medianBlur(g, 3).astype(float))
    print(f"{r}  media={media:.1f}  std={std:.1f}  saturados={sat:.2f}% ruido={ruido:.2f}")
