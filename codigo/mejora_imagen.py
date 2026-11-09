"""Funciones de la Actividad 1 (Visión Artificial, MIA UNIR): mejora de imagen
mediante operaciones elementales sobre imágenes nocturnas de Dark Face.

Convenciones:
- Las imágenes se manejan como uint8 en [0, 255]; los cálculos intermedios se
  hacen en float64 y se vuelve a uint8 con `_a_uint8` (redondeo + recorte), de
  modo que NumPy nunca desborda en silencio (uint8 + uint8 da la vuelta a 0).
- OpenCV carga en BGR; para mostrar con Matplotlib se convierte a RGB.
- Funciones puras: devuelven una imagen nueva y no modifican la entrada.
"""
from collections.abc import Callable
from dataclasses import dataclass, field
from math import ceil
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import shannon_entropy


# =====================================================================
# 1. Carga de imágenes
# =====================================================================

def _leer(ruta):
    # cv2.imread devuelve None (sin excepción) si la ruta o el formato fallan
    bgr = cv2.imread(str(ruta), cv2.IMREAD_COLOR)
    if bgr is None:
        print(f"No se pudo leer {ruta.name}")
        return None
    return {"bgr": bgr, "gris": cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)}


def cargar_imagenes(directorio, extensiones=(".jpg", ".jpeg", ".png")):
    """Todas las imágenes del directorio → {nombre: {"bgr": color, "gris": grises}}."""
    imgs = {}
    for ruta in sorted(Path(directorio).iterdir()):
        if ruta.suffix.lower() in extensiones and (d := _leer(ruta)) is not None:
            imgs[ruta.stem] = d
    return imgs


def cargar_imgs_propias(directorio, lista, extension="png"):
    """Solo las imágenes indicadas en `lista` (identificadores de Dark Face)."""
    imgs = {}
    for img in lista:
        ruta = Path(directorio) / f"{img}.{extension}"
        if (d := _leer(ruta)) is not None:
            imgs[ruta.stem] = d
    return imgs


# =====================================================================
# 2. Utilidades: métricas, figuras y luminancia
# =====================================================================

def metricas(img):
    """Métricas de calidad sobre la imagen en grises (o su luminancia), en uint8.

    - media: brillo medio μ.
    - contraste_rms: desviación típica σ de las intensidades.
    - michelson: (p99 − p1) / (p99 + p1), con percentiles 1 y 99 (robusto
      frente a píxeles aislados, a diferencia de max/min).
    - entropia: entropía de Shannon H = −Σ p_k log2 p_k (bits).
    - %_negro, %_blanco: porcentaje de píxeles saturados a 0 y a 255.
    """
    img = np.asarray(img)
    if img.ndim == 3:  # si llega en color, medir sobre la luminancia
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f = img.astype(np.float64)
    p1, p99 = np.percentile(f, [1, 99])
    return {
        "media": f.mean(),
        "contraste_rms": f.std(),
        "michelson": (p99 - p1) / (p99 + p1) if (p99 + p1) > 0 else 0.0,
        "entropia": shannon_entropy(img),
        "%_negro": 100 * np.mean(img == 0),
        "%_blanco": 100 * np.mean(img == 255),
    }


_NUCLEO_RUIDO = np.array([[ 1, -2,  1],
                          [-2,  4, -2],
                          [ 1, -2,  1]], dtype=np.float64)


def sigma_ruido(img):
    """Estimación de la desviación típica del ruido (Immerkær, 1996).

    σ = √(π/2) · Σ|f * N| / (6 (W−2)(H−2)), con N = [1 −2 1; −2 4 −2; 1 −2 1].
    N es la diferencia de dos laplacianos discretos: anula (casi) la estructura
    de la imagen y deja sobre todo el ruido. Se descarta el borde de 1 píxel.
    """
    r = cv2.filter2D(img.astype(np.float64), cv2.CV_64F, _NUCLEO_RUIDO)[1:-1, 1:-1]
    return np.sqrt(np.pi / 2) * np.abs(r).sum() / (6 * r.size)


def recorte(img, fila=0.35, col=0.35, alto=0.25, ancho=0.25):
    """Recorte relativo (fracciones del tamaño de la imagen)."""
    h, w = img.shape[:2]
    f0, c0 = int(fila * h), int(col * w)
    return img[f0:f0 + int(alto * h), c0:c0 + int(ancho * w)]


def a_rgb(img):
    return img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def histograma(ax, img, log=False):
    """Histograma de 256 niveles en `ax` (uno por canal si la imagen es en color)."""
    if img.ndim == 2:
        ax.hist(img.ravel(), bins=256, range=(0, 256), color="0.3", log=log)
    else:
        for i, c in enumerate(("b", "g", "r")):
            ax.hist(img[..., i].ravel(), bins=256, range=(0, 256), color=c,
                    alpha=0.4, log=log)
    ax.set_xlim(0, 255)
    ax.set_yticks([])
    ax.minorticks_off()


def comparar(imagenes_dict, titulo=None, guardar=None, filas=1, columnas=None,
             ancho_celda=4.0, figsize=None, con_histograma=True,
             alto_histograma=1 / 3, hist_log=False, tam_letra=None,
             mostrar=True, dpi=None):
    """Rejilla de imágenes, cada una con su histograma debajo.

    imagenes_dict   {"Original": img, "Gamma 0.5": img2, ...}; se colocan por filas.
    titulo          título general de la figura.
    guardar         ruta del PNG (p. ej. DIR_FIGS / "182_gamma.png"); None = no guardar.
    filas, columnas tamaño de la rejilla en «celdas» (imagen + histograma). Si se
                    omite `columnas`, se calcula como ⌈n / filas⌉; si se fija
                    `columnas` y no `filas`, filas = ⌈n / columnas⌉.
    ancho_celda     ancho en pulgadas de cada imagen; el alto se deduce de la
                    proporción alto/ancho de la primera imagen (sin huecos).
    figsize         tamaño total de la figura; si se da, ignora `ancho_celda`.
    con_histograma  False → solo las imágenes.
    alto_histograma alto del histograma relativo al de la imagen.
    hist_log        eje vertical del histograma en escala logarítmica (útil cuando
                    un pico en 0 aplasta el resto de niveles).
    tam_letra       tamaño de letra de los subtítulos (None = el de Matplotlib).
    mostrar         False → no llama a plt.show() (para seguir editando la figura).
    dpi             resolución del PNG guardado (None = la de rcParams).
    Devuelve (fig, ejes_img, ejes_hist): matrices filas × columnas de ejes;
    ejes_img[i, j] es la imagen de la celda (i, j) y ejes_hist[i, j] su
    histograma (ejes_hist = None si con_histograma=False).
    """
    n = len(imagenes_dict)
    if columnas is None:
        columnas = ceil(n / filas)
    elif filas is None or filas * columnas < n:
        filas = ceil(n / columnas)

    filas_por_celda = 2 if con_histograma else 1
    ratios = [1, alto_histograma] * filas if con_histograma else [1] * filas
    if figsize is None:
        h, w = next(iter(imagenes_dict.values())).shape[:2]
        # + 0.35 pulgadas por fila para los subtítulos
        figsize = (ancho_celda * columnas,
                   ancho_celda * h / w * sum(ratios) + 0.35 * filas)

    fig, axes = plt.subplots(filas * filas_por_celda, columnas, figsize=figsize,
                             gridspec_kw={"height_ratios": ratios}, squeeze=False)
    ejes_img = axes[::filas_por_celda]
    ejes_hist = axes[1::2] if con_histograma else None

    for k in range(filas * columnas):
        i, j = divmod(k, columnas)
        if k >= n:  # celdas sobrantes de la rejilla
            ejes_img[i, j].axis("off")
            if con_histograma:
                ejes_hist[i, j].axis("off")
            continue
        etiqueta, img = list(imagenes_dict.items())[k]
        ejes_img[i, j].imshow(a_rgb(img), cmap="gray", vmin=0, vmax=255)
        ejes_img[i, j].set_title(etiqueta, fontsize=tam_letra)
        ejes_img[i, j].axis("off")
        if con_histograma:
            histograma(ejes_hist[i, j], img, log=hist_log)

    if titulo:
        fig.suptitle(titulo)
    fig.tight_layout()
    if guardar:
        fig.savefig(guardar, bbox_inches="tight", dpi=dpi)
    if mostrar:
        plt.show()
    return fig, ejes_img, ejes_hist


def sobre_luminancia(bgr, f):
    """Aplica f(uint8 2D) → uint8 2D solo al canal Y de YCrCb y conserva la crominancia."""
    ycrcb = cv2.cvtColor(bgr, cv2.COLOR_BGR2YCrCb)
    ycrcb[..., 0] = f(ycrcb[..., 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)


@dataclass(frozen=True)
class Tecnica:
    """Técnica con sus parámetros fijados: t(img) la aplica y str(t) da su etiqueta.

    Solo envuelve una función de la sección 3 (que no se modifica) para que el
    valor aplicado y el que se imprime en figuras y tablas sean el mismo.
    Los parámetros se pasan por posición, en el orden de `params`, así que las
    claves pueden ser etiquetas («γ», «k») en vez de los nombres de los argumentos.

        t = Tecnica(correccion_gamma, "Gamma", {"γ": 0.6})
        t(img)   # ≡ correccion_gamma(img, 0.6)
        str(t)   # 'Gamma (γ = 0.6)'
    """
    f: Callable
    nombre: str
    params: dict = field(default_factory=dict)

    def __call__(self, img):
        return self.f(img, *self.params.values())

    def __str__(self):
        if not self.params:
            return self.nombre
        # :g evita etiquetas como 0.35000000000000003 (típicas de np.linspace)
        valores = ", ".join(f"{k} = {v:g}" for k, v in self.params.items())
        return f"{self.nombre} ({valores})"

    def __rshift__(self, otra):
        # t1 >> t2: primero t1, luego t2
        return Cadena((self,)) >> otra


@dataclass(frozen=True)
class Cadena:
    """Composición de técnicas T = T_n ∘ … ∘ T_1: aplica los pasos en orden.

    Se comporta como una Tecnica (c(img) la aplica, str(c) da la etiqueta), así
    que sirve en cualquier sitio donde se use una. Se construye con >>:

        c = Tecnica(correccion_gamma, "Gamma", {"γ": 0.5}) >> Tecnica(ecualizacion_global, "Ecualización global")
        str(c)   # 'Gamma (γ = 0.5) → Ecualización global'

    El orden importa (en general T_2 ∘ T_1 ≠ T_1 ∘ T_2) y cada paso devuelve
    uint8, de modo que entre pasos se redondea y se recorta a [0, 255]: lo que
    un paso satura ya no lo recupera el siguiente.
    """
    pasos: tuple

    def __call__(self, img):
        for t in self.pasos:
            img = t(img)
        return img

    def __str__(self):
        return " → ".join(str(t) for t in self.pasos)

    def __rshift__(self, otra):
        # cadena >> técnica (o >> otra cadena): añade los pasos al final
        extra = otra.pasos if isinstance(otra, Cadena) else (otra,)
        return Cadena(self.pasos + extra)


# =====================================================================
# 3. Técnicas de mejora (uint8 → uint8)
# =====================================================================

def _a_uint8(x):
    """Redondea y recorta a [0, 255] antes de volver a uint8 (evita desbordamientos)."""
    return np.clip(np.rint(x), 0, 255).astype(np.uint8)


def negativo(img):
    # s = (L − 1) − r = 255 − r
    return 255 - img


def estiramiento_lineal(img, p_inf=1, p_sup=99):
    # s = 255 · (r − r_min) / (r_max − r_min), con r_min y r_max = percentiles
    r_min, r_max = np.percentile(img, (p_inf, p_sup))
    if r_max <= r_min:               # imagen plana: nada que estirar
        return img.copy()
    return _a_uint8((img.astype(np.float64) - r_min) * 255.0 / (r_max - r_min))


def transformacion_log(img):
    # s = c · log(1 + r), con c = 255 / log(1 + r_max) para que la salida llegue a 255
    r_max = float(img.max())
    if r_max == 0:
        return img.copy()
    c = 255.0 / np.log1p(r_max)
    return _a_uint8(c * np.log1p(img.astype(np.float64)))


def correccion_gamma(img, gamma):
    # s = 255 · (r / 255)^γ ; γ < 1 aclara, γ > 1 oscurece. Se precalcula la LUT
    # de 256 entradas y se aplica por indexación.
    lut = _a_uint8(255.0 * (np.arange(256) / 255.0) ** gamma)
    return cv2.LUT(img, lut)


def ecualizacion_global(img):
    # s_k = round(255 · (F(k) − F(k_0)) / (1 − F(k_0))), con F(k) = Σ_{j≤k} p(j) la
    # distribución acumulada empírica y k_0 el primer nivel con píxeles: el primer
    # nivel ocupado va a 0 y el último a 255 (los píxeles a 0 siguen en 0)
    return cv2.equalizeHist(img)


def suma_constante(img, k):
    # s = r + k, saturando a [0, 255]
    return _a_uint8(img.astype(np.float64) + k)


def multiplicacion_constante(img, k):
    # s = k · r, saturando a [0, 255]
    return _a_uint8(img.astype(np.float64) * k)


# Núcleos discretos de ∇²f = ∂²f/∂x² + ∂²f/∂y² por diferencias centrales:
#   ∂²f/∂x² ≈ f(x+1,y) − 2f(x,y) + f(x−1,y)  (análogo en y; la 8-vecindad añade las diagonales)
_NUCLEO_LAPLACIANO = {
    4: np.array([[0,  1, 0],
                 [1, -4, 1],
                 [0,  1, 0]], dtype=np.float64),
    8: np.array([[1,  1, 1],
                 [1, -8, 1],
                 [1,  1, 1]], dtype=np.float64),
}


def laplaciano(img, vecindad=4, sigma=0.0):
    """∇²(G_σ * f) en float64.

    - sigma = 0: laplaciano discreto de f.
    - sigma > 0: laplaciano de la gaussiana (LoG); el suavizado previo G_σ atenúa
      el ruido antes de derivar, porque ∇² es un filtro paso alto.
    Devuelve float64 SIN recortar: ∇²f toma valores negativos (rango aprox. ±1020
    con 4-vecindad), que en uint8 se perderían.
    """
    f = img.astype(np.float64)
    if sigma > 0:
        f = cv2.GaussianBlur(f, (0, 0), sigma)
    # filter2D calcula una correlación; como el núcleo es simétrico coincide con la convolución
    return cv2.filter2D(f, cv2.CV_64F, _NUCLEO_LAPLACIANO[vecindad])


def realce_laplaciano(img, c=1.0, vecindad=4, sigma=0.0):
    """g = f − c · ∇²(G_σ * f), saturando a [0, 255].

    El signo menos se debe a que el centro del núcleo es negativo: restar ∇²f
    sube f donde la intensidad tiene un máximo local (lado claro de un borde)
    y la baja en el lado oscuro, acentuando la transición.
    Solo se suaviza el término de detalle; f se suma sin suavizar.
    Con c = 1, vecindad 4 y σ = 0 equivale a convolucionar con [0 −1 0; −1 5 −1; 0 −1 0].
    """
    g = img.astype(np.float64) - c * laplaciano(img, vecindad, sigma)
    return _a_uint8(g)
