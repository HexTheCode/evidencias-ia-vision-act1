# Configuración LaTeX para la memoria

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-05 18:38 CET |
| Fin | 2026-11-05 18:39 CET |
| Conversación | `e81b29ba-6887-4fe8-bdb2-c4a02a086c16` |
| Mensajes del autor | 1 |
| Llamadas a herramientas | Projects ×3, memory_read ×1 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 18:38

**Autor:**

> Mi plan es escribir la memoria de esta actividad en Latex. El profesor pide un formato científico. Hazme un propmt para Claude Code para que me prepare el set up del documento en Latex.

**Claude:**

Voy a revisar el enunciado de la actividad en el proyecto para que el prompt se ajuste a lo que pide el profesor.

- `[Proyecto] project_info`
- `[Memoria] va-actividad-1.md`
- `[Proyecto] project_read muinar03_act1.pdf`
- `[Proyecto] project_read Rúbrica_MIA_VA_act1.pdf`

Aquí tienes el prompt, adaptado a lo que piden el enunciado y la rúbrica. Rellena lo que va entre `[corchetes]` antes de pegarlo:

```text
Quiero que prepares el esqueleto (set up) de un documento LaTeX para la memoria
de un laboratorio de Visión Artificial (máster en IA, UNIR). NO escribas el
contenido de la memoria: solo la estructura, la configuración y marcadores de
posición comentados. Yo redactaré el texto.

## Contexto
- Actividad: "Laboratorio. Mejora de imagen: operaciones elementales".
  Mejoro 4 imágenes nocturnas de la base de datos The Dark Face con
  transformaciones de intensidad, procesamiento de histograma y operaciones
  aritméticas, y comparo las técnicas.
- El código está en Python con OpenCV, en [ruta del repo/carpeta del código].
- Sistema: Arch Linux. Compilaré en local.
- Idioma del documento: español.

## Requisitos de formato (los evalúa la rúbrica)
- Formato de artículo científico, entregado en PDF.
- Extensión: entre 8 y 12 páginas reales. Elige márgenes, tamaño de letra
  (10–11 pt) y columnas (pregúntame si una o dos) pensando en ese rango.
- Cabecera/título con: Asignatura (Visión Artificial), Apellidos, Nombre
  ([mis datos]) y Fecha.
- Toda la descripción de algoritmos debe ser formal y sin vincularse a un
  lenguaje de programación → usa un entorno de pseudocódigo
  (algorithm + algpseudocode o algorithm2e) y ecuaciones con amsmath.
- TODO el código debe ir en anexos, numerados, titulados y referenciados
  desde el texto. Inclúyelo desde los ficheros .py reales (no copiado a mano),
  con resaltado de sintaxis de Python.

## Estructura obligatoria (secciones en este orden)
1. Resumen (abstract) + palabras clave
2. Introducción
3. Material y métodos (subsecciones: software y entorno; conjunto de
   imágenes y características: origen, resolución, profundidad de color;
   técnicas de mejora; procedimiento experimental paso a paso)
4. Resultados (análisis comparativo antes/después, histogramas, métricas
   de contraste en tablas)
5. Conclusiones
6. Declaración sobre el uso de IA
7. Referencias
8. Anexos (código y material complementario)

En cada sección deja un comentario breve con lo que debe contener según el
enunciado, para guiarme al redactar.

## Aspectos técnicos
- Organiza el proyecto en ficheros: main.tex, preamble.tex (o .sty),
  sections/*.tex, figures/, tables/, code/ (o enlace a la carpeta del
  código), refs.bib.
- Bibliografía con biblatex + biber en estilo [IEEE / APA]. Mete en refs.bib
  como entradas de ejemplo: el artículo de Dark Face (Yang, W. et al., 2020,
  IEEE Transactions on Image Processing, 29, 5737–5752) y el libro de
  Gonzalez & Woods, Digital Image Processing. Verifica los datos.
- Figuras: subcaption para mostrar original vs. procesada (y su histograma)
  lado a lado. Crea una macro o ejemplo reutilizable para esa comparación.
- Tablas: booktabs, con una tabla de ejemplo para métricas por imagen y
  técnica.
- Referencias cruzadas con cleveref (en español) y hyperref.
- Siglas/unidades: siunitx.
- Compilación con latexmk: añade un .latexmkrc y un Makefile (o script) con
  targets para compilar y limpiar. Añade un .gitignore para los auxiliares.
- Si usas minted, configura -shell-escape y dime qué dependencia de Python
  hace falta; si no, usa listings con un estilo legible.
- Indícame qué paquetes de Arch (texlive-*, biber, etc.) necesito instalar
  con pacman, comprueba cuáles ya tengo y NO instales nada sin preguntarme.

## Al terminar
- Compila el documento y comprueba que no hay errores ni warnings
  importantes (referencias indefinidas, overfull boxes graves).
- Dime cuántas páginas ocupa el esqueleto y explícame en pocas líneas cómo
  añadir una figura, una tabla, una cita, un algoritmo y un anexo de código.
```

Un par de detalles que conviene que decidas antes de lanzarlo: el estilo de citas (IEEE encaja mejor con un artículo técnico, APA también se acepta) y si quieres una o dos columnas; a dos columnas cabe más, pero con muchas figuras comparativas a una columna suele leerse mejor y llegar a las 8 páginas es más fácil.

Cuando tengas el esqueleto, la sección que más pesa en la nota es Resultados (3,5 puntos), así que merece la pena planificar pronto qué figuras y métricas vas a incluir.
