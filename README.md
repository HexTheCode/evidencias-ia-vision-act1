# Evidencias de uso de IA · Visión Artificial, Actividad 1

Este repositorio recoge las conversaciones con asistentes de IA mantenidas durante la
**Actividad 1, «Mejora de imagen: operaciones elementales»**, de la asignatura *Visión
Artificial* del Máster Universitario en Inteligencia Artificial (UNIR). Sirve de respaldo
a la **declaración sobre el uso de IA** de la memoria, que enlaza aquí.

**Autor:** Antonio López García · **Periodo:** del 5 al 9 de noviembre de 2026

## Resumen

- **10 sesiones de Claude Code**, con 70 prompts del autor en total.
- **10 conversaciones en claude.ai**, con 21 mensajes del autor en total.
- **Reparto del trabajo:** Claude escribió y refactorizó el código Python (técnicas de
  mejora, métricas, figuras y tablas) y montó la infraestructura LaTeX. El análisis de
  resultados, los hallazgos y la mayor parte del texto de la memoria son del autor; en esos
  textos Claude corrigió la ortografía y propuso mejoras, y el autor decidió cuáles aplicar.
- **Fragmentos redactados por Claude a petición del autor**, revisados por el autor:
  definiciones formales de Material y métodos, párrafos breves de la Introducción y notas
  puntuales. Cada caso consta en la transcripción correspondiente.

## Herramientas

| Herramienta | Versión / modelo | Uso |
|---|---|---|
| Claude Code (CLI, Arch Linux) | Claude Code 2.1.318–2.1.319 · modelo Claude Opus 5.5 (`claude-opus-5-5`) | Código Python y cuadernos Jupyter, documento LaTeX, revisión de textos |
| Claude en claude.ai | Proyecto de la asignatura con el enunciado, la rúbrica y los materiales del curso · el export no indica el modelo | Dudas sobre requisitos y teoría, primer esqueleto del cuaderno y funciones, prompt y `CLAUDE.md` para Claude Code |

El autor llevó además, durante la actividad, un **registro propio de uso de IA por tarea**:
[USO_IA.md](USO_IA.md).

## Índice de sesiones

### Claude en claude.ai

| Fecha | Herramienta | Tarea | Transcripción |
|---|---|---|---|
| 2026-11-05 | claude.ai | Resumen de los requisitos de la actividad y teoría de la ecualización del histograma | [2026-11-05_resumen-actividad-ecualizacion.md](claude-ai/2026-11-05_resumen-actividad-ecualizacion.md) |
| 2026-11-05 | claude.ai | Elección entre Python con OpenCV y MATLAB; esqueleto del cuaderno (carga de imágenes, métricas, visualización) | [2026-11-05_python-opencv-o-matlab.md](claude-ai/2026-11-05_python-opencv-o-matlab.md) |
| 2026-11-05 | claude.ai | Método reproducible de selección de las imágenes y corrección de un error en el script del autor | [2026-11-05_seleccion-imagenes.md](claude-ai/2026-11-05_seleccion-imagenes.md) |
| 2026-11-05 | claude.ai | Orientación para la función negativo a partir del cuaderno de laboratorio | [2026-11-05_funcion-negativo.md](claude-ai/2026-11-05_funcion-negativo.md) |
| 2026-11-05 | claude.ai | Prompt para que Claude Code montara el esqueleto LaTeX de la memoria | [2026-11-05_configuracion-latex.md](claude-ai/2026-11-05_configuracion-latex.md) |
| 2026-11-05 | claude.ai | Implementación de las funciones de técnicas pendientes del cuaderno | [2026-11-05_metodos-pendientes.md](claude-ai/2026-11-05_metodos-pendientes.md) |
| 2026-11-06 | claude.ai | Redacción del `CLAUDE.md` con el contexto para Claude Code | [2026-11-06_contexto-claude-code.md](claude-ai/2026-11-06_contexto-claude-code.md) |
| 2026-11-09 | claude.ai | Tipos de ecualización de histogramas en el temario | [2026-11-09_tipos-ecualizacion.md](claude-ai/2026-11-09_tipos-ecualizacion.md) |
| 2026-11-09 | claude.ai | Formato de la entrega: tipo de letra e interlineado | [2026-11-09_tipo-letra-interlineado.md](claude-ai/2026-11-09_tipo-letra-interlineado.md) |
| 2026-11-09 | claude.ai | Requisitos: si el estiramiento no lineal es obligatorio | [2026-11-09_estiramiento-no-lineal.md](claude-ai/2026-11-09_estiramiento-no-lineal.md) |

### Claude Code

| Fecha | Herramienta | Tarea | Transcripción |
|---|---|---|---|
| 2026-11-05 | Claude Code | Esqueleto del documento LaTeX: estructura, preámbulo, macros, `Makefile`, bibliografía verificada y `CLAUDE.md` | [2026-11-05_esqueleto-latex.md](claude-code/2026-11-05_esqueleto-latex.md) |
| 2026-11-06 | Claude Code | Configuración de VS Code para usar el entorno virtual del cuaderno | [2026-11-06_entorno-vscode-venv.md](claude-code/2026-11-06_entorno-vscode-venv.md) |
| 2026-11-06 | Claude Code | Implementación del realce laplaciano en el cuaderno (las conclusiones son del autor) | [2026-11-06_realce-laplaciano.md](claude-code/2026-11-06_realce-laplaciano.md) |
| 2026-11-06 | Claude Code | Coordinación de los proyectos LaTeX y de cuadernos; corrección y propuestas de mejora de la Introducción y de Material y métodos; palabras clave y tablas | [2026-11-06_revision-introduccion-metodos.md](claude-code/2026-11-06_revision-introduccion-metodos.md) |
| 2026-11-08 | Claude Code | Contraste RMS; registro de los hallazgos del autor sobre la corrección gamma; clases `Tecnica` y `Cadena`; cuaderno de experimentos | [2026-11-08_gamma-hallazgos-funciones.md](claude-code/2026-11-08_gamma-hallazgos-funciones.md) |
| 2026-11-08 | Claude Code | Función de comparativa múltiple; respuestas del autor a las preguntas de discusión y corrección de sus argumentos | [2026-11-08_comparativas-multiples.md](claude-code/2026-11-08_comparativas-multiples.md) |
| 2026-11-08 | Claude Code | Paso de los hallazgos a la memoria LaTeX (tablas, figuras, referencia) y correcciones | [2026-11-08_integrar-hallazgos-latex.md](claude-code/2026-11-08_integrar-hallazgos-latex.md) |
| 2026-11-09 | Claude Code | Revisión de la memoria: definiciones formales de métodos, retirada de CLAHE, corrección de Resultados, citas cruzadas y registro formal | [2026-11-09_revision-memoria.md](claude-code/2026-11-09_revision-memoria.md) |
| 2026-11-09 | Claude Code | Estructura del documento, posición de figuras y revisión de las Conclusiones | [2026-11-09_estructura-conclusiones.md](claude-code/2026-11-09_estructura-conclusiones.md) |
| 2026-11-09 | Claude Code | Recopilación del uso de IA en la actividad y cómo evidenciarlo | [2026-11-09_extraccion-uso-ia.md](claude-code/2026-11-09_extraccion-uso-ia.md) |

## Código de la actividad

La carpeta [`codigo/`](codigo/) contiene el código con el que se obtuvieron los resultados
de la memoria. Es el mismo que se incluye en sus anexos.

| Fichero | Contenido |
|---|---|
| [`mejora_imagen.py`](codigo/mejora_imagen.py) | Funciones de carga, técnicas de mejora, métricas y figuras (Anexo A) |
| [`act1_mejora_imagen.ipynb`](codigo/act1_mejora_imagen.ipynb) | Cuaderno principal: aplica las técnicas y genera las figuras y tablas de la memoria (Anexo B) |
| [`img_extraction.py`](codigo/img_extraction.py) | Selección de las 4 imágenes entre una muestra de 100 del dataset (Anexo C) |
| [`act1_experimentos.ipynb`](codigo/act1_experimentos.ipynb) | Cuaderno de pruebas exploratorias (no aporta resultados a la memoria) |
| [`requirements.txt`](codigo/requirements.txt) | Versiones de las librerías usadas (Python 3.12.15) |

Los cuadernos se publican **sin salidas**: contienen imágenes de Dark Face, que no se
redistribuyen. Para reproducir los resultados, coloca las imágenes del dataset en `imgs/`
junto al código y ejecuta los cuadernos.

## Qué contiene cada transcripción

- **Incluido:**
  - Mensajes del autor, completos.
  - Respuestas de texto de Claude, completas.
  - Cada llamada a herramienta resumida en una línea, p. ej. `[Edit] Actividad 1/LaTeX/sections/03-resultados.tex`.
  - Respuestas del autor a preguntas de Claude y herramientas rechazadas por el autor.
- **Omitido:**
  - Salidas de las herramientas.
  - Contenido de los ficheros leídos o escritos.
  - Imágenes.
  - Razonamiento interno del modelo.
  - Contexto que Claude Code añade automáticamente (instrucciones de sistema, recordatorios).
  - En claude.ai, el contenido de los ficheros adjuntos (solo se indica su nombre) y los
    resultados de las búsquedas en el proyecto, la memoria y los chats anteriores.
- **Anonimización:**
  - Las rutas absolutas se sustituyen por rutas relativas a `Actividad 1/` o por `~`.
  - Los directorios temporales de Claude Code se sustituyen por `<tmp>/`.
  - En claude.ai, las rutas del entorno de ejecución se sustituyen por `<tmp>/`,
    `<adjuntos>/` y `<proyecto>/`.

## Estructura

```
evidencias-ia/
├── README.md                    este fichero
├── USO_IA.md                    registro de uso de IA llevado por el autor durante la actividad
├── codigo/                      código Python y cuadernos de la actividad (sin salidas)
├── claude-code/                 transcripciones de Claude Code (AAAA-MM-DD_tema.md)
├── claude-ai/                   transcripciones de claude.ai (AAAA-MM-DD_tema.md)
└── scripts/
    ├── exportar_sesiones.py     conversor .jsonl → .md (solo biblioteca estándar)
    └── sesiones.json            sesiones exportadas y sus títulos
```

## Reproducir la exportación

Las sesiones de Claude Code se guardan localmente en `~/.claude/projects/<carpeta del proyecto>/<id>.jsonl`.
Con esos ficheros presentes, basta con ejecutar:

```bash
python3 scripts/exportar_sesiones.py            # regenera claude-code/*.md
python3 scripts/exportar_sesiones.py --indice   # lista numerada de prompts por sesión
```

Las conversaciones de claude.ai salen del `conversations.json` del export de la cuenta
(Settings → Privacy → Export data):

```bash
python3 scripts/exportar_sesiones.py --claude-ai ~/ruta/conversations.json   # regenera claude-ai/*.md
```

La configuración privada opcional se lee de `scripts/privado.json`, que no se publica.
