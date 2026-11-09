# Coordinación LaTeX/cuadernos y revisión de Introducción y Material y métodos

| | |
|---|---|
| Herramienta | Claude Code 2.1.319 |
| Modelo | claude-opus-5-5 |
| Inicio | 2026-11-06 11:19 CET |
| Fin | 2026-11-06 13:03 CET |
| Carpeta de trabajo | `Actividad 1`, `Actividad 1/notebooks`, `Actividad 1/LaTeX` |
| Sesión | `36b7118e-207a-47ea-b0e5-9312366dc43c` |
| Prompts del autor | 9 |
| Llamadas a herramientas | Bash ×30, NotebookEdit ×15, Read ×4, Write ×3, Edit ×3, ToolSearch ×1 |

> Transcripción generada con `scripts/exportar_sesiones.py`. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus salidas, el contenido de ficheros, las imágenes y el razonamiento interno del modelo.

---

## Prompt 1 · 11:19

**Autor:**

> `/model`

---

## Prompt 2 · 11:23

**Autor:**

> En las dos subcarpetas latex y notebooks hay proyectos de claude code que trabajan por separado. Uno escribir un documento el latex, el otro el código necesario para escribir ese documento. Te ejecuto en la carpeta raiz para que puedas ver los dos proyectos. Lee los CLAUDE.md antes de nada.
> 1. Extrae todo el código de funciones fuera del notebook en un archivo python a parte
> 2. Me gustaría tener más control en la funcion comparar para crear plots (decidir cuantas filas tendrá el plot, etc.)
> 3. Lee el documento el latex e integra en las tablas los resultados que ya se han obtenido del csv creado por el notebook
> - Preguntame si tienes alguna duda
> - En tu mensaje final contandome lo que has hecho se muy breve (bullet points)

**Claude:**

- `[Bash] cd "Actividad 1"; find . -path ./notebooks/.venv -prune -o -type f -not -path '*/.git/*' -print | grep -v -E …`
- `[Bash] cd "Actividad 1"; cat LaTeX/CLAUDE.md; echo ----; cat notebooks/USO_IA.md; echo ----; cat notebooks/resultado…`

Now the notebook.

- `[Bash] cd "Actividad 1/notebooks"; python3 -c " …`
- `[Bash] cd "Actividad 1/LaTeX"; cat main.tex Makefile; for f in tables/*.tex sections/*.tex; do echo "===== $f"; cat …`
- `[Bash] cd "Actividad 1/LaTeX"; grep -n -i "unicode\|multirow\|siunitx\|sisetup" -A0 preamble.tex; cd ../notebooks; .…`

Ahora escribo el módulo.

- `[Write] Actividad 1/notebooks/mejora_imagen.py`

Corrijo el final del docstring de `comparar`, que había quedado mal redactado.

- `[Edit] Actividad 1/notebooks/mejora_imagen.py`
- `[ToolSearch] select:NotebookEdit`
- `[Read] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb (delete)`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb (delete)`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb (delete)`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb (delete)`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`

Ejecuto el notebook entero para comprobar que corre y que las métricas no cambian.

- `[Bash] cd "Actividad 1/notebooks"; cp figures/tabla_metricas.csv $CLAUDE_JOB_DIR/tmp/antes.csv; cp figures/tabla_rea…`
- `[Read] Actividad 1/notebooks/figures/182_resumen.png`

Las imágenes son 3:2 y la celda 4:3, así que sobra hueco. Hago que el alto por defecto salga de la proporción de la imagen.

- `[Bash] cd "Actividad 1/notebooks"; python3 - <<'EOF' …`
- `[NotebookEdit] Actividad 1/notebooks/act1_mejora_imagen.ipynb`
- `[Bash] cd "Actividad 1/notebooks"; .venv/bin/jupyter nbconvert --to notebook --execute act1_mejora_imagen.ipynb --ou…`
- `[Read] Actividad 1/notebooks/figures/182_resumen.png`

La rejilla ya no tiene huecos grandes. Ahora relleno las tablas LaTeX a partir de los CSV.

- `[Bash] cd "Actividad 1/LaTeX"; .venv=../notebooks/.venv; ../notebooks/.venv/bin/python - <<'EOF' …`
- `[Bash] cd "Actividad 1/LaTeX"; grep -n "bitpp\|DeclareSIUnit" preamble.tex`
- `[Bash] cd "Actividad 1/LaTeX"; python3 - <<'EOF' …`

Compila. Añado el módulo nuevo a los anexos (enlace simbólico, como `img_extraction.py`).

- `[Bash] cd "Actividad 1/LaTeX"; ln -s ../../notebooks/mejora_imagen.py code/mejora_imagen.py && python3 - <<'EOF' …`

Faltan caracteres Unicode del código (ya ocurría con el laplaciano). Los declaro en `preamble.tex` como indica el CLAUDE.md.

- `[Edit] Actividad 1/LaTeX/preamble.tex`
- `[Bash] cd "Actividad 1/LaTeX"; make 2>&1 | grep -E -i "^!|error|Unicode|Overfull|Output written" | sort | uniq -c | …`

Reviso visualmente la tabla de métricas en el PDF.

- `[Bash] cd "Actividad 1/LaTeX"; for p in 1 2 3 4 5; do pdftotext -f $p -l $p main.pdf - | grep -q "Realce laplaciano"…`
- `[Bash] cd "Actividad 1/LaTeX"; pdftoppm -f 3 -l 3 -r 80 -png main.pdf $CLAUDE_JOB_DIR/tmp/p`
- `[Read] ~/.claude/jobs/36b7118e/tmp/p-03.png`

Tabla correcta. Actualizo los CLAUDE.md y `USO_IA.md`.

- `[Bash] cd "Actividad 1"; python3 - <<'EOF' …`

He hecho las tres cosas. El notebook se ejecuta entero, los CSV salen idénticos a los de antes y la memoria compila sin errores ni overfull boxes.

- **1. Funciones fuera del notebook:** todas están ahora en `notebooks/mejora_imagen.py` y el notebook solo las importa y las usa. En la memoria he añadido el módulo como anexo propio (`anx:codigo-funciones`) mediante un enlace simbólico en `LaTeX/code/`, igual que `img_extraction.py`.
- **2. `comparar` con más control:** puedes elegir `filas` y `columnas`, el tamaño (`ancho_celda`, con el alto calculado según la proporción de la imagen, o `figsize`), si sale el histograma, su alto y si va en escala logarítmica, el tamaño de letra, `guardar` (ahora recibe una ruta, no `nombre_fichero`), `dpi` y `mostrar`. Devuelve `fig, ejes_img, ejes_hist` por si quieres retocar la figura. Las rejillas resumen ya salen en 2 filas.
- **3. Tablas LaTeX:** `tables/metricas.tex` y `tables/imagenes.tex` tienen ya los valores de `tabla_metricas.csv`. En la de métricas he añadido una fila de **realce laplaciano** por imagen, porque está en el CSV; si no la quieres en la tabla, se quita fácilmente.
- **Tablas a mano:** los valores están escritos directamente en los `.tex`, así que si cambias parámetros en el notebook habrá que volver a volcarlos.
- **Caracteres del código:** añadí en `preamble.tex` varios símbolos del código (π, Σ, −, √, ∂, ∇, ⌈ ⌉) porque pdfLaTeX fallaba con ellos.
- **Documentación:** he actualizado los dos `CLAUDE.md` y he añadido una línea en `USO_IA.md`.
- **Pendiente:**
  - La tabla `tabla_realce_laplaciano.csv` no tiene tabla en la memoria; ¿quieres que la cree?
  - El cuerpo sigue en 4 páginas de las 8–12 exigidas.

---

## Prompt 3 · 11:52

**Autor:**

> Aquí tienes la introducción del documento de LATex.
> - Corrige las faltas de ortografía sin cambiar las palabras ni el significado de las oraciones.
> - Propon mejoras antes de incluirlas en el documento
> - Se breve con tu explicación
>
>
>
> **[Texto pegado por el autor:]**
>
> Introducción 
>
> El preprocesamiento de imágenes es fundamental hoy en día, no solo para el análisis visual humano de fotografías en areas como la medicina (mamografías, TACs, etc.), sino que también para su preparación al analizarlas con métodos más avanzados (por ejemplo VLM). Es esencial para capturar información relevante que a primera vista no se distinga del propio ruido de fondo. Este artículo se centrá en el realce de imágenes mediante transformaciones píxel a píxel. Las técnicas utiliadas se resumen por sus objetivos. Uno de ellos es remarcar el contenido de una imagen con ruido en los casos de figura contra fondo y fondo contra figura. Otro de ellos es aumentar el nivel de contraste de una imagen, para diferenciar con más nitidez los elementos que se esconden en ella. Otro de ellos es delimitar visiblemente los bordes entre objetos dentro de la imagen, con el fin de segregarlos con mayor facilidad. Un ejemplo de este último objetivo sería la detección de páginas de papel en una imagen para delimitar su borde para un posterior escaneo. Dado que el papel común es blanco, es fácil como humanos, distinguir su borde del resto de la imagen. Sin embargo, para un ordenador es necesario implementar una de estos métodos de preprocesamiento, para que pueda distinguir sin problema la hoja de papel. Como se verá en este documento, muchas de las técnicas utilizadas para el realce de las imagenes, tendrán un efecto negativo en la calidad de las imágenes resultantes. En ocasiones se resaltarán unos elementos de la imagen en otras los complementarios a estos. También es probable la aparición de más ruido en la imagen resultante, en comparación de la imagen original. 
> &lt;/pasted_content id="3eb8">

**Claude:**

- `[Edit] Actividad 1/LaTeX/sections/01-introduccion.tex`
- `[Bash] cd "Actividad 1/LaTeX"; make 2>&1 | grep -E "^!|Error|Overfull|Output written" | tail -3; make paginas`
- `[Bash] cd "Actividad 1"; echo "- 2026-11-06 · Introducción · La redacté yo; Claude solo corrigió ortografía y puntua…`

He metido tu introducción en `LaTeX/sections/01-introduccion.tex` con solo las faltas de ortografía y de puntuación corregidas. No he cambiado ninguna palabra y la memoria compila. Debajo dejé el recuadro `\pendiente` que ya había; bórralo cuando quieras.

**Lo que he corregido:**
- Tildes: áreas, imágenes.
- Erratas: centrá → centrará, utiliadas → utilizadas.
- Comas:
  - «por ejemplo, VLM»
  - «es fácil, como humanos, distinguir»
  - Quité la coma entre sujeto y verbo en «…de las imágenes tendrán».
  - «En ocasiones se resaltarán unos elementos de la imagen; en otras, los complementarios…»

**Mejoras que te propongo (no he aplicado ninguna):**
1. **Gramática:** cambian alguna palabra, por eso no las he tocado.
   - «sino que también» → «sino también»
   - «una de estos métodos» → «uno de estos métodos»
   - «en comparación de» → «en comparación con»
   - «TACs» → «TAC» (la RAE lo deja igual en plural)
2. **Siglas:** explica qué es VLM la primera vez (modelos de visión y lenguaje).
3. **Repeticiones:** «Uno de ellos… Otro de ellos… Otro de ellos» se puede cambiar por «En primer lugar… En segundo lugar… Por último».
4. **Vocabulario técnico:** «segregarlos» → «segmentarlos» o «separarlos».
5. **Párrafos:** es un solo bloque. Podrías separarlo en tres: contexto, objetivos de las técnicas y limitaciones.
6. **Lo que falta según la plantilla y la rúbrica:**
   - Hablar de imágenes nocturnas y de Dark Face con su cita (`\cite{yang2020darkface}`). Ahora no se mencionan.
   - El marco teórico con su cita (`\cite{gonzalez2018dip}`).
   - El objetivo concreto: 4 imágenes, tres familias de técnicas y comparar cuál funciona mejor.
   - Un párrafo que explique cómo está organizado el documento, con `\cref{sec:metodos,sec:resultados,sec:conclusiones}`.
7. **Ejemplo:** el del papel se entiende bien, pero se aleja del tema. Uno sobre detectar caras de noche (el fin de Dark Face) lo conectaría mejor con el resto.

Dime cuáles quieres y las aplico. También he añadido una línea en `USO_IA.md`.

---

## Prompt 4 · 11:57

**Autor:**

> 1.  cambia solo unos, comparacion con, TAC
> 2. hazlo
> 3. hazlo
> 4. hazlo
> 5. hazlo
> 6. Incluye marco teórico (breve), objetivo concreto (breve) , hablar de imágenes nocturas (breve)
> 7. Quita el ejemplo

**Claude:**

- `[Bash] cd "Actividad 1/LaTeX"; sed -n '/\\section{Introducción}/,$p' sections/01-introduccion.tex | tail -6`
- `[Bash] cd "Actividad 1/LaTeX"; python3 - <<'EOF' …`

He aplicado en la introducción (`LaTeX/sections/01-introduccion.tex`) todo lo que elegiste, y la memoria compila sin errores:

1. Cambié «uno de estos», «en comparación con» y «TAC». La frase de «uno de estos métodos» estaba dentro del ejemplo del papel, así que ha desaparecido con él (punto 7).
2. VLM ahora aparece como «modelos de visión y lenguaje, VLM».
3. «En primer lugar… En segundo lugar… Por último».
4. «segmentarlos».
5. El texto queda en 5 párrafos: contexto e imágenes nocturnas, marco teórico, objetivos de las técnicas, limitaciones y objetivo del trabajo.
6. He añadido tres partes cortas escritas por mí; revísalas, porque son las únicas frases que no has escrito tú:
   - **Imágenes nocturnas:** qué las hace difíciles y la cita de Dark Face.
   - **Marco teórico:** s = T(r), qué técnicas entran en esa familia y la cita de Gonzalez.
   - **Objetivo:** las 4 imágenes, las tres familias de técnicas y la comparación visual y con métricas.
7. He quitado el ejemplo del papel.

Solo queda un recuadro `\pendiente` en la sección: la estructura del documento, que no pediste. También he añadido una línea en `USO_IA.md`.

---

## Prompt 5 · 12:40

**Autor:**

> Siguiente texto: Material y métodos.
> - Propon correccion de faltas de ortografía
> - Propon mejoras
> - Preguntar antes de aplicar
> - Se breve
>
>
>
>
> **[Texto pegado por el autor:]**
>
> Material y métodos
>
> Como sowftware se ha utilizado una combinación de herramientas. La báse del código está en Python y junto a el se usan las librerías: pandas, opencv, matplotlib. Las librerías pandas y matplotlib son utilizadas para la creación de tablas y gráficas comparativas al aplicar transformaciones a las imagenes, y la librería opencv se encarga de procesar dichas imágenes. Todo el código se ejecuta de forma interactiva en Jupiter Notebook y los resultados se guardan en tablas en archivos .csv o en imágenes en el caso de los gráficos comparativos. Mediante un script en python se ha comparado una muestra aleatoría (con una semilla preestablecida) de 100 imágenes entre el total del dataset (un total de 600 imágenes), fijandose en métricas concretas: la media de los píxeles, la desviación estandar de los píxeles, el procentaje de saturación y el ruido. Entre todas ellas, se han elegido las imágenes siguiente los siguientes casos:
> 1. Imagen muy oscura y de bajo contraste. 
> 2. Imagen oscura con focos de luz.
> 3. Imagen con más luz y contraste comprimido.
> 4. Imagen ruidosa.
> Las imágenes escogidas, en orden, han sido: 182, 5069, 5940, 5019. Esta metodología para la selección de imagenes para su posterior procesado, se ha aplicado conociendo la importancia de la replicabilidad de los resultados, así como proporcionar un análisis poco sesgado y que abarca muchos casos de imágenes diferentes en el dataset.
> &lt;/pasted_content id="3eb8">

**Claude:**

- `[Bash] cd "Actividad 1/notebooks"; ls imgs | wc -l; .venv/bin/python -c " …`
- `[Bash] cd "Actividad 1/notebooks"; grep -E "/(182|5069|5940|5019|81)\.png" resultados.txt`

Propuestas para *Material y métodos*. No he cambiado nada en el documento.

**Faltas de ortografía**
- sowftware → software
- báse → base
- junto a el → junto a él
- imagenes → imágenes (aparece 2 veces)
- Jupiter → Jupyter
- python → Python
- opencv → OpenCV (es nombre propio)
- aleatoría → aleatoria
- fijandose → fijándose
- estandar → estándar
- procentaje → porcentaje
- «las imágenes siguiente los siguientes casos» → «siguiendo los siguientes casos»
- «para su posterior procesado, se ha aplicado» → sin coma
- «que abarca» → «que abarque»
- «así como proporcionar» → «así como la de proporcionar»

**Datos que no cuadran con el código**
1. El dataset tiene **6000** imágenes, no 600 (lo he comprobado en `imgs/`).
2. La muestra tiene **101** imágenes: `img_extraction.py` añade `81.png` a mano después del muestreo aleatorio. O lo cuentas en el texto o quitas esa línea del script.
3. Faltan **NumPy** y **scikit-image**, que se usa para la entropía. Versiones del `.venv`: Python 3.12.15, OpenCV 5.0.0, NumPy 2.5.4, pandas 3.1.1, Matplotlib 3.11.2, scikit-image 0.26.0.
4. Las medias de la selección (`resultados.txt`) no coinciden del todo con las de la tabla de imágenes: 182 da 3,0 frente a 3,3 y 5940 da 39,0 frente a 39,5. El script de selección lee las imágenes directamente en grises y el notebook las convierte a grises desde color, y no lo hacen igual. Convendría usar en ambos la misma conversión.

**Mejoras**
5. **Definir las métricas de selección de forma formal.** «Saturación» es el porcentaje de píxeles con valor ≥ 250. «Ruido» es σ(f − mediana₃ₓ₃(f)). Además, este estimador de ruido no es el de Immerkær que se usa después: o se explica o se unifica.
6. **Criterio de elección.** Explica cómo se pasa de la muestra de 101 a las 4 imágenes: por ejemplo, la de menor media, la de mayor % de saturados, la de mayor ruido… La 5019 tiene el mayor ruido de la muestra (10,97).
7. **Tabla de imágenes.** Añadir dos columnas, «% saturados» y «ruido», a la tabla de imágenes (`tab:imagenes`) para apoyar los 4 casos con datos.
8. **Estructura.** La rúbrica pide subsecciones: el primer párrafo va en *Software y entorno* y el resto en *Conjunto de imágenes*. La lista de casos quedaría como `enumerate`, con referencias al código (`\cref{anx:seleccion}`, `\cref{anx:codigo-funciones,anx:codigo-notebook}`) y a la tabla de imágenes (`\cref{tab:imagenes}`).
9. **Faltan contenidos** de la sección *Conjunto de imágenes*:
   - Qué es Dark Face, con su cita.
   - Resolución, número de canales y formato, remitiendo a la tabla de imágenes.
   - Por qué se trabaja en escala de grises.
10. **Matizar la última frase.** Con 4 imágenes es difícil decir que se «abarcan muchos casos». Sería más justo algo como «cubre situaciones representativas».

¿Qué aplico?

---

## Prompt 6 · 12:47

**Autor:**

> 0. Corrige las faltas
> 1. OK
> 2. No lo menciones eso solo fue una prueba, quita esa modificación al script
> 3. OK
> 4. Cambia el script entonces, para que se asemeje al notebook. Ejecutalo otro vez para verificar, no vaya a ser que salgan otras imágenes como mejor candidatas.
> 5. Ok explicalo siendo muy breve
> 6. Ok explicalo siendo muy breve
> 7. OK
> 8. OK añade las subsecciones, no inventes texto nuevo.
> 9. OK se muy breve
> 10. Modifica el texto, cambia lo que dije por: cubre situaciones representativas

**Claude:**

- `[Bash] cd "Actividad 1/notebooks"; cat img_extraction.py; cp resultados.txt $CLAUDE_JOB_DIR/tmp/resultados_antes.txt`
- `[Write] Actividad 1/notebooks/img_extraction.py`
- `[Bash] cd "Actividad 1/notebooks"; .venv/bin/python img_extraction.py > resultados.txt; wc -l resultados.txt; .venv/…`

Misma muestra de 100 imágenes; ahora las medias coinciden con el notebook y 5019 sigue siendo la más ruidosa. Escribo la sección.

- `[Bash] cd "Actividad 1/LaTeX"; python3 - <<'EOF' …`
- `[Bash] cd "Actividad 1"; grep -c Overfull LaTeX/build/main.log; echo "- 2026-11-06 · Material y métodos · Texto mío;…`

He aplicado los 10 puntos en `LaTeX/sections/02-material-metodos.tex`. La memoria compila sin errores ni overfull boxes y el cuerpo va por 5 páginas de 8–12.

- **0. Faltas:** corregidas todas las de la lista.
- **2 y 4. Script de selección:**
  - He quitado la imagen 81 de `img_extraction.py`.
  - Ahora convierte a grises igual que el notebook.
  - Lo he vuelto a ejecutar: sale la misma muestra de 100 y las medias ya coinciden con la tabla de imágenes. `resultados.txt` está regenerado.
- **Ojo con la selección:** la 5019 sigue siendo la más ruidosa y la 5940 la de menor σ entre las imágenes con μ > 30. Pero hay dos que no son el caso extremo de la muestra:
  - **182:** hay imágenes más oscuras (1182, 2416, 1711, con μ < 1).
  - **5069:** la 4091 y la 2144 tienen más píxeles saturados (0,50 % frente a 0,41 %).

  Por eso el texto describe esas dos con sus valores y no dice que sean el máximo. Si tienes un motivo para haberlas elegido (por ejemplo, que las de μ < 1 son casi negras y no se recupera nada), conviene añadirlo.
- **3. Software:** he añadido NumPy y scikit-image y las versiones de todas las librerías.
- **5 y 6. Textos nuevos (muy breves):**
  - Qué es la saturación (píxeles ≥ 250) y cómo se mide el ruido (residuo respecto al filtro de mediana 3×3), aclarando que esa medida solo se usa para elegir las imágenes.
  - Detrás de cada uno de los 4 casos, entre paréntesis, el valor que lo justifica.
- **7. Tabla de imágenes:** tiene ahora las columnas «% sat.» y «Ruido».
- **8. Subsecciones:** he repartido tu texto entre *Software y entorno* y *Conjunto de imágenes*, con la lista de casos numerada y las referencias a los anexos y a la tabla.
- **9. Añadido (breve):**
  - Origen: Dark Face, con su cita.
  - Formato: PNG de 1080×720, 3 canales.
  - Por qué se trabaja en grises: un solo canal y un solo histograma.
- **10. Última frase:** ahora termina en «…y que cubre situaciones representativas del dataset».

He añadido también una línea en `USO_IA.md`.

---

## Prompt 7 · 13:00

**Autor:**

> Cambios que te pido para el documento de LAtex:
> 1. Añade palabras clave creibles (Computer Vision, OpenCV, Imagen processing, etc.)
> 2. Tabla 2 con todas ls técnicas aplicadas ponla en el anexo D. Ya se hará una tabla resumen que ocupará su lugar con las técnicas más relevantes. Ahora deja puesto un placeholder en su lugar.

**Claude:**

- `[Bash] cd "Actividad 1/LaTeX"; python3 - <<'EOF' …`
- `[Bash] cd "Actividad 1/LaTeX"; grep -E "undefined|Reference" build/main.log | head; latexmk >/dev/null 2>&1; grep -c…`
- `[Bash] cd "Actividad 1"; echo "- 2026-11-06 · Palabras clave y tablas · Claude propuso las palabras clave a partir d…`

He hecho los dos cambios y la memoria compila sin errores ni referencias rotas.

1. **Palabras clave:** visión artificial; procesamiento de imágenes; imágenes con baja iluminación; ecualización de histograma; corrección gamma; OpenCV. Las he puesto en español porque la memoria está en español; si las prefieres en inglés, las cambio.
2. **Tabla completa de técnicas:** ahora está en el **Anexo D** (Material complementario) como Tabla 3.
   - En *Resultados* (Métricas de contraste) queda un recuadro con el título «Tabla resumen pendiente», que ahora es la Tabla 2. Remite a la tabla completa y está en `tables/metricas-resumen.tex`, donde pegarás las filas de las técnicas que elijas.
   - El recuadro se ve siempre, también con `\borradorfalse`, para que no se te olvide rellenarlo.
   - El cuerpo de la memoria baja a **4 páginas** (objetivo 8–12), porque la tabla grande ha salido de él.

---

## Prompt 8 · 13:03

**Autor:**

> Estupedo. Cierro sessión.

**Claude:**

- `[Write] ~/.claude/projects/-home-<usuario>-Desktop-M-ster-Visi-n-Artificial-Actividad-1/memory/revision-textos-memori…`
- `[Bash] echo "- [Revisión de textos de la memoria](revision-textos-memoria.md) — corregir, proponer numerado, pregunt…`

Perfecto, hasta la próxima. Te dejo lo que quedó pendiente:

- **Rellenar la tabla resumen** en `LaTeX/tables/metricas-resumen.tex` con las técnicas que elijas.
- **Estructura del documento:** queda un recuadro pendiente al final de la introducción.
- **Imágenes 182 y 5069:** conviene justificar por qué se eligieron, porque no son las más extremas de la muestra.
- **Faltan páginas:** el cuerpo tiene 4 y la rúbrica pide 8–12.

Me he guardado en memoria cómo quieres que revise tus textos: corregir, proponer numerado y preguntar antes de aplicar.

---

## Prompt 9 · 13:03

**Autor:**

> `/exit`
