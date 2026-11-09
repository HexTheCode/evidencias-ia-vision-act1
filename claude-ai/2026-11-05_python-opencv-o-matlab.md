# Python con OpenCV o MATLAB y esqueleto del cuaderno

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-05 10:49 CET |
| Fin | 2026-11-05 11:18 CET |
| Conversación | `8b093c9a-ad64-465e-ad1c-abc7d7d85f4e` |
| Mensajes del autor | 3 |
| Llamadas a herramientas | Bash ×4, Projects ×2, Write ×1, Read ×1, SendUserFile ×1 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 10:49

**Autor:**

> Tengo una duda, el profesor ha dicho que podemos hacer el código en python con opencv o en matlab con el toolkit específico. Estoy en arch linux y aquí cuesta instalar matlab en local pero tengo acceso a matlab online. Cuales de las opciones me recomiendas?

**Claude:**

- `[Proyecto] project_search «actividad 1 enunciado entrega»`
- `[Proyecto] project_read muinar03_act1.pdf`

Te recomiendo **Python con OpenCV** (más NumPy, Matplotlib y scikit-image), salvo que quieras ir lo más pegado posible a los ejemplos del profesor.

**Por qué Python en tu caso**
- **En Arch se instala sin problemas.** `sudo pacman -S python-opencv python-numpy python-matplotlib python-scikit-image jupyterlab` y tienes todo en local. No dependes del navegador ni de subir las imágenes de Dark Face a MATLAB Drive.
- **El enunciado no te ata al lenguaje.** Pide que en *Material y métodos* describas las técnicas "sin depender de lenguajes de programación concretos". Solo tienes que indicar qué software usaste, así que ninguna opción puntúa más que la otra.
- **Te sirve más allá de la asignatura.** OpenCV y NumPy son lo estándar en visión artificial e ingeniería. Los vas a reutilizar en el resto del máster y probablemente en el TFM.
- **Cubre todas las técnicas de la actividad:**
  - Negativo, logaritmo, gamma y operaciones aritméticas: con NumPy son una línea cada una.
  - Estiramiento lineal: `skimage.exposure.rescale_intensity`, equivalente a `imadjust`/`stretchlim`.
  - Gamma y logaritmo con funciones ya hechas: `exposure.adjust_gamma` y `exposure.adjust_log`.
  - Ecualización: `cv2.equalizeHist` (global) y `cv2.createCLAHE` (adaptativa, como `adapthisteq`). CLAHE suele dar muy buen resultado con imágenes nocturnas como las de Dark Face.

**Cuándo elegiría MATLAB Online**
- Si quieres copiar casi tal cual los `.mlx` del laboratorio (`t6_negativo`, `t6_correccion_gamma`, `t6_ecualizacion_histograma`…) y que tus resultados coincidan con los de las sesiones de refuerzo.
- Si no te apetece escribir tú las funciones de apoyo. Una antes/después con histograma, por ejemplo, en MATLAB sale casi gratis con `imhist` y `montage`.
- Antes de elegirlo, comprueba si tu cuenta tiene licencia de la UNIR. Sin licencia, MATLAB Online tiene horas de uso limitadas al mes, y para un laboratorio con varias pruebas puede quedarse corto.

**Mi sugerencia práctica:** hazlo en Python, en un notebook de Jupyter. Usa los `.mlx` como guía de qué hace cada técnica y qué parámetros prueba el profesor, y tradúcelos. Así entiendes mejor cada transformación, que es justo lo que necesitas para la parte de comparación y limitaciones de la memoria.

Si te parece bien, el siguiente paso es montar la estructura del notebook: carga de las 4 imágenes, una función que muestre antes/después con histogramas y un par de métricas de contraste (media, desviación típica, entropía). ¿Empezamos por ahí?

---

## Mensaje 2 · 10:53

**Autor:**

> Sí hazlo yo voy preparando el setup

**Claude:**

Voy a montar el notebook con la carga de imágenes, la visualización antes/después y las métricas, y lo pruebo antes de pasártelo.

- `[Bash] python -c "import cv2, numpy, matplotlib, skimage, pandas, nbformat; print('ok')" 2>&1 || pip install --break…`
- `[Bash] for m in cv2 numpy matplotlib skimage pandas scipy jupyter nbclient ipykernel; do python -c "import $m; print…`
- `[Bash] cd <adjuntos>/ && pdftotext -layout 17eef230-R_brica_MIA_VA_act1.pdf - | head -80`
- `[Write] <tmp>/scratchpad/build_nb.py`

Ahora lo pruebo con imágenes nocturnas sintéticas, incluyendo un caso con farola saturada.

- `[Bash] S=<tmp>/scratchpad; mkdir -p $S/test/imagenes && cd $S/test && python $S/build_nb.py $S/test/act1_mejora_imag…`
- `[Read] <tmp>/scratchpad/test/figuras/noche_0_original.png`
- `[Fichero enviado] Esqueleto del notebook: carga, métricas, figuras y tabla listas; las técnicas quedan como TODO para ti.`

He preparado `act1_mejora_imagen.ipynb` y lo he probado de principio a fin con imágenes nocturnas sintéticas: genera las figuras y la tabla sin errores.

**Para ponerlo en marcha:**
- Junto al notebook, crea una carpeta `imagenes/` y mete dentro tus 4 imágenes de Dark Face.
- Si te falta algo: `sudo pacman -S python-scikit-image python-pandas jupyterlab`.
- Las figuras y la tabla `tabla_metricas.csv` se guardan solas en `figuras/`.

**Lo que ya funciona:**
- Carga de las imágenes y tabla de características (resolución, canales, tipo), que te sirve para *Material y métodos*.
- Función `comparar()`, que muestra antes y después con el histograma debajo de cada imagen.
- Función `metricas()`, que calcula:
  - brillo medio y contraste RMS,
  - contraste de Michelson usando los percentiles 1 y 99,
  - entropía,
  - % de píxeles saturados a 0 o a 255 (sirve para detectar artefactos como farolas quemadas).
- Función `sobre_luminancia()`, por si decides trabajar en color.
- Bucle final que construye la tabla comparativa y la rejilla resumen de cada imagen.

**Lo que te toca a ti:** las 8 funciones de las técnicas, que están como `TODO`. Te he dejado una tabla de equivalencias MATLAB → Python para traducir los `.mlx` del laboratorio.

Dos cosas de la rúbrica que conviene tener presentes desde ya:
- La memoria tiene que ocupar entre 8 y 12 páginas, y todo el código va en los anexos.
- Material y métodos no puede mencionar ningún software concreto.

Una decisión que te recomiendo tomar antes de empezar: ¿trabajas en escala de grises o sobre la luminancia en color? Tendrás que justificarla en la memoria.

Cuando tengas las imágenes elegidas, empieza por el negativo y la gamma, que son las más sencillas. Si algo no te cuadra, me lo enseñas.

---

## Mensaje 3 · 11:18

**Autor:**

> como instalo paquetes pip en un uv venv

**Claude:**

Con `uv` no se usa `pip` directamente, sino `uv pip`. Desde la carpeta donde está el `.venv`:

```bash
uv venv                      # crea .venv (si no lo tienes ya)
uv pip install opencv-python scikit-image pandas matplotlib jupyterlab
```

No hace falta activar el entorno: `uv pip` detecta solo el `.venv` del directorio actual. Para ejecutar algo dentro del entorno, actívalo con `source .venv/bin/activate` o usa `uv run jupyter lab`.

Si escribes `pip install` a secas con el entorno activado, puede fallar o instalar en el Python del sistema. Los venv de `uv` no traen `pip` salvo que los crees con `uv venv --seed`.

**Alternativa como proyecto**, que te deja un `pyproject.toml` con las dependencias y es más reproducible:

```bash
uv init
uv add opencv-python scikit-image pandas matplotlib jupyterlab
uv run jupyter lab
```

Para el notebook, si abres Jupyter con `uv run jupyter lab` ya usa ese entorno y no tienes que registrar ningún kernel aparte.
