# Función negativo del cuaderno

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-05 12:32 CET |
| Fin | 2026-11-05 12:41 CET |
| Conversación | `f668b1e1-e707-4303-b7e8-7541b9943429` |
| Mensajes del autor | 3 |
| Llamadas a herramientas | Projects ×2, Bash ×2, memory_read ×1 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 12:32

**Autor:**

> Me puedes ayudar a hacer la función negativo del notebook

**Claude:**

- `[Memoria] va-actividad-1.md`
- `[Proyecto] project_info`
- `[Proyecto] project_read Materiales prácticos/Laboratorio/t6_negativo.mlx`
- `[Bash] mkdir -p <tmp>/scratchpad/neg && cd <tmp>/scratchpad/neg && unzip -o -q "<adjuntos>/f690c910-t6_negativo.mlx"…`
- `[Bash] pdftotext -layout "<adjuntos>/a20cb27a-muinar03_act1.pdf" - | head -120; pdftotext "<adjuntos>/a3835fc4-Tema_…`

Antonio, he mirado el notebook `t6_negativo.mlx` y la parte del negativo del Tema 6. Te guío para que lo traduzcas tú a Python/OpenCV.

**1. La teoría (Tema 6)**

La transformación es s = (L − 1) − r, donde L es el **número de niveles de intensidad**. En una imagen de 8 bits, L = 256, así que s = 255 − r. El tema dice que sirve para realzar estructuras claras dentro de zonas oscuras. Eso te viene bien para comentarlo en la memoria con Dark Face.

**2. Un detalle del notebook que no deberías copiar**

El `.mlx` hace `L = max(I(:))` y luego `I_neg = (L - 1) - I`. Eso no coincide con la teoría. Si el máximo de la imagen es, por ejemplo, 200, salen valores negativos, y al convertir a `uint8` se recortan a 0. De hecho, la gráfica final del propio notebook usa `255 - r`. Usa L = 256, o sea, 255 − r.

**3. Los pasos que tiene que hacer tu función**

Equivalen a lo que hace el notebook:
1. Leer la imagen con `cv2.imread`. Ojo, OpenCV la carga en **BGR**.
2. Aplicar la transformación.
3. Calcular los histogramas de la original y del resultado.
4. Mostrar las dos imágenes, sus histogramas y la curva de transformación s(r).

**4. Pistas para la implementación**

- Si la imagen es `uint8`, `255 - img` funciona directamente con NumPy y no se desborda, porque nunca baja de 0. También existe `cv2.bitwise_not(img)`, que da el mismo resultado. Puedes usar cualquiera de las dos y justificar la elección.
- Las imágenes de Dark Face son **en color**, y aquí hay una decisión de diseño que conviene explicar en la memoria:
  - aplicarlo a los tres canales a la vez, lo que invierte también los colores;
  - o pasar a HSV/LAB e invertir solo la luminancia (V o L), lo que conserva el tono.
- Para el histograma tienes `cv2.calcHist([img], [0], None, [256], [0, 256])` o `np.histogram`. Normalízalo dividiendo entre el número de píxeles, como hace el notebook.
- Para mostrar, con matplotlib en una cuadrícula 2×2. Acuérdate de `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` antes de `imshow`.

**5. Un esqueleto para que lo rellenes**

```python
def negativo(img: np.ndarray) -> np.ndarray:
    """Devuelve el negativo s = (L-1) - r de una imagen uint8."""
    # TODO: comprobar dtype y aplicar la transformación
    ...
```

Sería bueno dejar la visualización en una función aparte, por ejemplo `mostrar_resultado(original, procesada, titulo)`. Así podrás reutilizarla con el resto de técnicas: gamma, logaritmo, estiramiento y ecualización.

**Para que lo pienses:** con imágenes nocturnas, el negativo por sí solo no suele "mejorar" la imagen. ¿Qué crees que pasa con el histograma de una imagen de Dark Face al aplicarlo? Esa reflexión encaja con el objetivo de la actividad de comparar técnicas y sus limitaciones.

Cuando tengas tu versión, pégamela y la revisamos. Si te atascas, también te puedo dar el código completo.

---

## Mensaje 2 · 12:40

**Autor:**

> pasame el código de solo como lees la imagen con cv2, para despues hacerle la trasnformación.

**Claude:**

```python
import cv2
import numpy as np

ruta = "imagenes/mi_imagen.png"  # cambia por la ruta de tu imagen de Dark Face

img = cv2.imread(ruta, cv2.IMREAD_COLOR)  # se carga en BGR, uint8
if img is None:
    raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")

print(img.shape, img.dtype)  # p. ej. (720, 1080, 3) uint8
```

`cv2.imread` no lanza ningún error si la ruta es incorrecta, solo devuelve `None`. Por eso conviene la comprobación del `if`.

Si quieres trabajar en escala de grises, como en el notebook de MATLAB, usa `cv2.IMREAD_GRAYSCALE` en lugar de `cv2.IMREAD_COLOR`. Así obtienes una matriz 2D de tipo `uint8`.

Con `img` cargada como `uint8`, ya puedes aplicarle directamente la transformación s = 255 − r.

---

## Mensaje 3 · 12:41

**Autor:**

> Y como sería con una imagen ya cargada y con us datos en un array?

**Claude:**

Si ya tienes la imagen en un array de NumPy, la transformación es una sola operación vectorizada que se aplica a todos los píxeles a la vez:

```python
def negativo(img: np.ndarray) -> np.ndarray:
    """Negativo s = (L-1) - r para una imagen de 8 bits (L = 256)."""
    if img.dtype != np.uint8:
        raise TypeError(f"Se esperaba uint8 y llegó {img.dtype}")
    return 255 - img

img_neg = negativo(img)
```

Qué conviene tener en cuenta:

- **Funciona igual en gris y en color.** Si `img` tiene forma `(alto, ancho)` o `(alto, ancho, 3)`, NumPy aplica la resta a cada elemento, así que en color invierte los tres canales.
- **No hay desbordamiento.** Como `r` está entre 0 y 255, `255 - r` también, y el resultado sigue siendo `uint8`.
- **Comprobar el `dtype` es importante.** Si el array fuera `float` en [0, 1], por ejemplo tras normalizarlo, la fórmula correcta sería `1.0 - img`. Si fuera `uint16`, sería `65535 - img`. El `raise` evita que apliques la fórmula equivocada sin darte cuenta.
- **Equivalente en OpenCV:** `cv2.bitwise_not(img)` da exactamente lo mismo en `uint8`.

Ahora te quedaría la parte de los histogramas y la visualización. ¿Quieres intentarla tú primero?
