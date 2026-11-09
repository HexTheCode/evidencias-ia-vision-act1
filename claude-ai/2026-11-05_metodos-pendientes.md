# Código de los métodos pendientes del cuaderno

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-05 18:44 CET |
| Fin | 2026-11-05 18:57 CET |
| Conversación | `bdeebd72-7613-4171-84e4-d4a1752cfa12` |
| Mensajes del autor | 2 |
| Llamadas a herramientas | conversation_search ×2, memory_read ×1, Projects ×1, recent_chats ×1, Bash ×1 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 18:44

**Autor:**

> Dame el código de todos los métodos del notebook que no has construido aún

**Claude:**

- `[Memoria] va-actividad-1.md, index.md`
- `[Proyecto] project_info`
- `[Chats recientes] 10`
- `[Buscar en chats] «TODO funciones técnicas notebook»`
- `[Buscar en chats] «tecnicas correccion_gamma suma_constante tabla comparativa bucle»`
- `[Bash] cat > /tmp/t.py <<'EOF' …`

Aquí tienes las 7 funciones que faltan (el `negativo` ya lo hicimos). Sustituye la celda de los `TODO` por esto; las he probado con una imagen oscura sintética y todas devuelven `uint8` en [0, 255]:

```python
import numpy as np
import cv2

def _a_uint8(x):
    """Redondea y recorta a [0, 255] antes de volver a uint8 (evita desbordamientos)."""
    return np.clip(np.rint(x), 0, 255).astype(np.uint8)

def negativo(img):
    return 255 - img

def estiramiento_lineal(img, p_inf=1, p_sup=99):
    # s = 255 · (r - r_min) / (r_max - r_min), con r_min y r_max = percentiles
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
    # s = 255 · (r / 255)^γ ; γ < 1 aclara (lo que buscas en Dark Face), γ > 1 oscurece
    lut = _a_uint8(255.0 * (np.arange(256) / 255.0) ** gamma)
    return cv2.LUT(img, lut)

def ecualizacion_global(img):
    return cv2.equalizeHist(img)

def ecualizacion_adaptativa(img, clip=2.0, rejilla=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=rejilla)
    return clahe.apply(img)

def suma_constante(img, k):
    # s = r + k, saturando a [0, 255]
    return _a_uint8(img.astype(np.float64) + k)

def multiplicacion_constante(img, k):
    # s = k · r, saturando a [0, 255]
    return _a_uint8(img.astype(np.float64) * k)
```

Después, en la celda de la sección 4, descomenta las líneas del diccionario `tecnicas` y ya se genera la tabla y las rejillas.

Algunas decisiones que tendrás que justificar en *Material y métodos*:

- **Gamma con LUT.** Como solo hay 256 niveles posibles, se calcula la curva una vez y se aplica como tabla de consulta. Es exacto y rápido.
- **Log con `c` adaptado a cada imagen.** Si usaras `c = 255 / log(256)` fijo, en una imagen con máximo 60 la salida no pasaría de ~190. Lo calculo con el máximo real, así que es una elección que debes explicar.
- **Estiramiento con percentiles 1–99** en lugar de mínimo y máximo. Así unas pocas farolas o píxeles muertos no anulan el estiramiento, a cambio de saturar ese 2 % extremo. Lo verás en la columna `%_blanco` de las métricas.
- **Suma y multiplicación** saturan igual que `imadd`/`immultiply` de MATLAB. La multiplicación conserva el negro, y la suma lo levanta, que en imágenes oscuras se nota como un "velo" gris.

Una cosa que falta en el notebook: la rúbrica también nombra el **estiramiento no lineal** (`t6_estiramiento_no_lineal.mlx`) y el esqueleto no tiene función para él. Si quieres, lo traducimos ahora del `.mlx`.

---

## Mensaje 2 · 18:57

**Autor:**

> Porqué en la tabla comparativa pone **metricas

**Claude:**

Es el operador de **desempaquetado de diccionarios** de Python. Dentro de un `{...}`, `**d` mete todos los pares clave-valor de `d` en el diccionario que estás construyendo.

`metricas()` devuelve un diccionario, algo así:

```python
metricas(img)
# {"brillo": 12.4, "contraste_rms": 29.5, "michelson": 0.93, "entropia": 5.1, ...}
```

Entonces esta línea:

```python
{"imagen": nombre, "técnica": tecnica, **metricas(f(d["gris"]))}
```

equivale a:

```python
{"imagen": nombre, "técnica": tecnica,
 "brillo": 12.4, "contraste_rms": 29.5, "michelson": 0.93, "entropia": 5.1, ...}
```

Es decir, une en **un solo diccionario plano** la identificación de la fila (imagen y técnica) con todas sus métricas. Así cada métrica acaba siendo una columna propia cuando haces `pd.DataFrame(filas)`.

Sin los `**`, escribirías `"metricas": metricas(...)` y tendrías una única columna llamada `metricas` con un diccionario dentro de cada celda, que no sirve para comparar ni para exportar a CSV.

Dos detalles:

- Si hubiera claves repetidas, gana la que aparece **más a la derecha**. Aquí no ocurre porque las métricas no se llaman `imagen` ni `técnica`.
- Es lo mismo que `dict(a, **b)` o que `a | b` (Python 3.9+). Con un solo asterisco, `*lista`, se desempaquetan listas o tuplas en vez de diccionarios.
