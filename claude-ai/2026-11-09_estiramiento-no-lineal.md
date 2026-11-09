# ¿Es obligatorio el estiramiento no lineal?

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-09 13:48 CET |
| Fin | 2026-11-09 13:49 CET |
| Conversación | `10f912bd-6139-4642-a0d9-bd14e4ee689f` |
| Mensajes del autor | 1 |
| Llamadas a herramientas | Projects ×2 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 13:48

**Autor:**

> Es obligatorio usar el estiramiento no lineal?

**Claude:**

- `[Proyecto] project_search «estiramiento no lineal actividad requisitos técnicas obligatorias»`
- `[Proyecto] project_read muinar03_act1.pdf`

No es obligatorio. Ni el enunciado ni la rúbrica nombran el estiramiento no lineal como técnica concreta que tengas que usar. Lo que sí piden es aplicar tres familias de técnicas:

- **Funciones de ajuste de intensidad.** Aquí entran el estiramiento lineal, el no lineal, la corrección gamma, la transformación logarítmica, el negativo…
- **Procesamiento del histograma**, por ejemplo la ecualización.
- **Operadores aritméticos.**

Tienes que tocar las tres familias, pero dentro de cada una eliges tú las técnicas.

Aun así, piensa en el tipo de imagen. Las de Dark Face tienen casi todos los píxeles amontonados en los tonos oscuros. Pregúntate qué hace un estiramiento lineal con un histograma así, y qué haría en cambio una transformación que levante mucho los oscuros y poco los claros. Si lo comparas, verás por qué una técnica no lineal (gamma con γ < 1, logarítmica, etc.) suele ser de las que mejor funcionan aquí.

Además, la rúbrica premia en Resultados que compares técnicas y discutas sus limitaciones. Comparar un ajuste lineal con uno no lineal en la misma imagen te da un análisis muy aprovechable. Así que no es obligatorio, pero probablemente te convenga incluirlo y justificar por qué lo eliges.

¿Qué técnicas tenías pensadas para el apartado de ajuste de intensidad?
