# Tipos de ecualización de histogramas en los temas

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-09 10:55 CET |
| Fin | 2026-11-09 10:56 CET |
| Conversación | `15b41aac-4c28-412c-ad90-a5caca931a22` |
| Mensajes del autor | 1 |
| Llamadas a herramientas | Bash ×4, Projects ×3 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 10:55

**Autor:**

> Cuantos tipos de ecualizaciones de histogramas hay en los temas?

**Claude:**

- `[Proyecto] project_search «ecualización del histograma tipos»`
- `[Proyecto] project_search «ecualización adaptativa CLAHE adapthisteq histeq especificación histograma»`
- `[Proyecto] project_read Materiales prácticos/Laboratorio/t6_ecualizacion_histograma.mlx`
- `[Bash] mkdir -p /tmp/mlx && cd /tmp/mlx && python3 -I -c " …`
- `[Bash] python3 -I -c " …`
- `[Bash] python3 -I -c " …`
- `[Bash] python3 -I -c " …`

En los temas solo aparece **un tipo**: la ecualización (o "igualación") de histograma **global y clásica**, explicada en el Tema 6, apartado 6.3 "Procesado sistemático del histograma".

La idea del tema es tratar cada píxel como una variable aleatoria y transformarla con su función de distribución para que quede uniforme. Como esa función no se conoce, se aproxima con el **histograma acumulado** normalizado. Así se mejora el contraste de forma automática, sin tener que ajustar a mano una función a trozos.

El material de laboratorio (`t6_ecualizacion_histograma.mlx`) usa ese mismo método con `histeq` de MATLAB. Hace tres cosas:
1. Ecualiza `image1.png` y compara el histograma de antes y el de después.
2. Dibuja la función de transformación que se aplicó, que es la CDF.
3. Vuelve a ecualizar la imagen ya ecualizada. Es un buen experimento para la memoria: ¿qué crees que pasa y por qué?

En ningún tema salen otras variantes conocidas, como la **ecualización adaptativa (AHE/CLAHE)** o la **especificación de histograma** (histogram matching). Si las quieres meter en la actividad 1, serían algo extra a lo que da el curso. En imágenes con poca luz, CLAHE suele funcionar mejor que la ecualización global. Si las usas, recuerda que la rúbrica te pide justificarlas y describirlas formalmente.
