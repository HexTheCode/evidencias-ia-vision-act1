# Contexto (CLAUDE.md) para Claude Code

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-06 11:08 CET |
| Fin | 2026-11-06 11:09 CET |
| Conversación | `02e33878-38f7-463e-b7c4-1529c6faa210` |
| Mensajes del autor | 1 |
| Llamadas a herramientas | Projects ×2, memory_read ×1, conversation_search ×1, Write ×1, SendUserFile ×1 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 11:08

**Autor:**

> Escríbeme un contexto para claude code en relación con el notebook, para poder dirigirlo en mi PC

**Claude:**

Voy a revisar el enunciado, la rúbrica y lo que ya tienes hecho del notebook para escribirte un CLAUDE.md a medida.

- `[Memoria] va-actividad-1.md, index.md`
- `[Proyecto] project_read muinar03_act1.pdf`
- `[Proyecto] project_read Rúbrica_MIA_VA_act1.pdf`
- `[Buscar en chats] «notebook OpenCV»`
- `[Write] /home/claude/CLAUDE.md`
- `[Fichero enviado] Ponlo en la raíz de la carpeta del notebook; Claude Code lo lee solo al arrancar.`

Te he escrito el `CLAUDE.md` para Claude Code. Guárdalo en la raíz de la carpeta del notebook, junto a `act1_mejora_imagen.ipynb` y la carpeta `imagenes/`. Claude Code lo lee solo al arrancar en esa carpeta.

Qué recoge:
- **Cómo debe ayudarte:** te guía en lugar de hacerlo por ti, salvo que se lo pidas expresamente, igual que en este proyecto.
- **El estado del notebook:** qué funciones ya existen (métricas, `comparar`, las 8 técnicas) y qué falta: el estiramiento no lineal y elegir y justificar los parámetros finales.
- **Normas de código:** trabajar en `uint8` con cálculos intermedios en float, que OpenCV carga en BGR, y que no toque las imágenes originales. También le dice que use `pacman`, no `pip`.
- **Lo que pide la rúbrica:** el código va en los anexos, *Material y métodos* no puede mencionar ningún software y *Resultados* es la sección que más puntúa.
- **Un registro de uso de IA:** le pide apuntar en `USO_IA.md` cada cosa importante que haga. Así tendrás el material para la declaración obligatoria de la memoria sin tener que reconstruirlo al final.

Si al abrirlo cambias algún nombre de archivo o función, actualízalo también en el `CLAUDE.md`. Si no, Claude Code se guiará por una estructura que ya no existe.
