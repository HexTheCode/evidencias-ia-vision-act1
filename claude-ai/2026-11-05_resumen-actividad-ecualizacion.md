# Resumen de la actividad y ecualización del histograma

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-05 10:15 CET |
| Fin | 2026-11-05 10:33 CET |
| Conversación | `4acd8049-3929-44e9-842a-773f90c44b4a` |
| Mensajes del autor | 3 |
| Llamadas a herramientas | Projects ×4 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 10:15

**Autor:**

> Hazme un resumen de lo que tengo que hacer en esta actividad

**Claude:**

- `[Proyecto] project_info`
- `[Proyecto] project_read muinar03_act1.pdf`
- `[Proyecto] project_read Rúbrica_MIA_VA_act1.pdf`

Antonio, la actividad 1 consiste en **mejorar imágenes nocturnas con técnicas elementales de procesamiento y entregar una memoria en formato de artículo científico**.

## Qué tienes que hacer

**1. Parte práctica**
- Elige **4 imágenes** de la base de datos **DARK FACE** (Yang et al., 2020). Son 6000 fotos reales tomadas de noche con poca luz, en calles, campus, puentes, parques, etc.
- Mejóralas aplicando las tres familias de técnicas del Tema 6, que la rúbrica nombra explícitamente:
  - **Funciones de ajuste de intensidad**: negativo, transformación logarítmica, corrección gamma, estiramiento lineal y no lineal.
  - **Procesamiento del histograma**: ecualización.
  - **Operadores aritméticos**: suma, resta, multiplicación o combinación de imágenes.
- **Compara** la eficacia de cada técnica en cada imagen e identifica sus limitaciones, como amplificación de ruido, saturación o artefactos. Después propón posibles soluciones.

Los cuadernos `t6_*.mlx` de la carpeta Laboratorio cubren justo estas técnicas, así que son tu punto de partida en MATLAB.

**2. Memoria (PDF, 8–12 páginas reales)**

| Sección | Peso | Qué debe contener |
|---|---|---|
| Resumen | 1 | Objetivo, técnicas aplicadas, hallazgos clave y relevancia práctica |
| Introducción | 1,5 | Importancia de mejorar imágenes con poca luz, aplicaciones (seguridad, medicina, teledetección…), qué es el preprocesamiento y objetivos justificados |
| Material y métodos | 2 | Software, las 4 imágenes (origen, resolución, profundidad de color) y cada técnica descrita **formalmente, con fórmulas y sin código**. El procedimiento debe ir paso a paso, ser replicable y justificar cada decisión |
| **Resultados** | **3,5** | Comparativa antes/después con figuras, histogramas, tablas e indicadores de contraste. Debe incluir análisis crítico, comparación entre técnicas, limitaciones y mejoras |
| Conclusiones | 1,5 | Qué técnica funcionó mejor y en qué imagen, limitaciones, artefactos y líneas futuras |
| Referencias | 0,5 | Formato APA o IEEE, actualizadas y variadas |

Ten en cuenta además estos requisitos:
- **Todo el código va en anexos**, nunca en el cuerpo del texto.
- **Declaración de uso de IA** al final, rigurosa y detallada: qué herramienta usaste, para qué tareas, cuál fue tu aportación y una reflexión crítica. Si no la declaras o es vaga, te penalizan.
- **Penalizaciones por formato**: no entregar en PDF, salirte de las 8–12 páginas o tener una estructura desordenada.

## Dónde poner el esfuerzo
**Resultados** es la sección que más pesa (3,5 de 10). Lo que da nota ahí es el **análisis crítico y la comparación entre técnicas**, más que la cantidad de imágenes. Un buen esquema sería una tabla por imagen con métricas como media, desviación típica (contraste) y entropía, acompañada de los histogramas antes y después.

¿Por dónde quieres empezar? Podemos elegir las 4 imágenes con criterio (por ejemplo, con distintos tipos de problema: muy oscura, con fuentes de luz puntuales, con ruido…) o repasar primero las técnicas del Tema 6.

---

## Mensaje 2 · 10:16

**Autor:**

> Son 4 o 6 imagenes lo que necesito

**Claude:**

Son **4 imágenes**. El enunciado dice que trabajarás con «cuatro imágenes seleccionadas por el alumno». El 6 sale de las **6000 imágenes** que tiene en total la base de datos DARK FACE, de entre las cuales eliges tus 4.

---

## Mensaje 3 · 10:32

**Autor:**

> Repasemos las técnicas del tema 6. Sobre todo la ecualización del histograma que no me quedó muy claro

**Claude:**

- `[Proyecto] project_search «ecualización del histograma función de distribución acumulada»`

Te hago primero un repaso rápido de todas las técnicas y luego nos centramos en la ecualización, que es la que más juego da con imágenes nocturnas.

## Mapa rápido del Tema 6

Casi todas son **transformaciones punto a punto**: cada píxel de entrada r se convierte en un valor de salida s = T(r) mediante una función T, sin mirar a sus vecinos. En lo que sigue, L es el número de niveles de gris (256 en imágenes de 8 bits) y c es una constante de escala.

| Técnica | Función | Efecto en una imagen oscura |
|---|---|---|
| Negativo | s = (L−1) − r | Invierte la imagen. No ilumina, pero a veces se ven mejor los detalles en zonas oscuras |
| Logarítmica | s = c·log(1 + r) | Expande los niveles oscuros y comprime los claros. Muy útil de noche |
| Gamma | s = c·r^γ | Con γ < 1 aclara las sombras y con γ > 1 las oscurece. Controlas la curva con un solo parámetro |
| Estiramiento lineal | Lleva el rango real [r_min, r_max] a [0, L−1] | Aprovecha todo el rango disponible. Falla si un solo píxel muy brillante (una farola) fija r_max |
| Estiramiento no lineal / a trozos | Curva definida por tramos | Control fino, pero los tramos se ajustan a mano, probando |
| **Ecualización** | s = (L−1)·F(r) | **Automática**: calcula la curva a partir de la propia imagen |
| Aritméticas | Suma, resta, producto entre imágenes | La suma promedia y reduce ruido, la resta detecta diferencias y el producto aplica máscaras |

## Ecualización del histograma

### La idea
Una imagen nocturna tiene casi todos sus píxeles amontonados en unos pocos niveles oscuros, así que el histograma es un pico pegado a la izquierda. La ecualización **reparte esos píxeles por todo el rango de grises** para que el histograma quede lo más plano posible. Más niveles distintos en uso significan más contraste.

### El fundamento
Te va a resultar familiar por la carrera, porque es la **transformada integral de probabilidad**. El tema modela la intensidad de cada píxel como una variable aleatoria Y. Si F es su función de distribución, la variable U = F(Y) es **uniforme en [0, 1]**.

El problema es que F no se conoce, así que se estima con el histograma:

1. **Histograma normalizado**: p(l) = n_l / N, donde n_l es el número de píxeles con nivel l y N el total de píxeles. Es la probabilidad empírica de cada nivel.
2. **Histograma acumulado**: F(l) = p(0) + p(1) + … + p(l). Es la función de distribución empírica.
3. **Transformación**: s = round((L−1)·F(r)).

### Ejemplo a mano
Imagina una imagen de 3 bits (L = 8 niveles) con 64 píxeles, muy oscura:

| Nivel r | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| n_r | 20 | 24 | 12 | 4 | 2 | 1 | 1 | 0 |
| Acumulado | 20 | 44 | 56 | 60 | 62 | 63 | 64 | 64 |
| F(r) | 0,31 | 0,69 | 0,88 | 0,94 | 0,97 | 0,98 | 1 | 1 |
| 7·F(r) | 2,19 | 4,81 | 6,13 | 6,56 | 6,78 | 6,89 | 7 | 7 |
| **s** | **2** | **5** | **6** | **7** | **7** | **7** | **7** | **7** |

Fíjate en tres cosas, porque son justo las que te servirán para el **análisis crítico** de la memoria:

- **Los niveles muy poblados se separan.** El 0 y el 1, que concentraban el 69 % de los píxeles, pasan a 2 y 5. Ahí está la ganancia de contraste.
- **Los niveles poco poblados se fusionan.** Los niveles 3 a 7 acaban todos en 7, así que **se pierde información** en las zonas claras.
- **El histograma resultante no sale plano.** En el caso discreto los píxeles de un mismo nivel se mueven juntos y no se pueden repartir entre varios niveles. Solo se consigue una uniformidad aproximada.

### Limitaciones en DARK FACE
- **Amplifica el ruido.** En las zonas oscuras el ruido del sensor ocupa los niveles más poblados, que son justo los que más se estiran. Prepárate para ver mucho grano.
- **Es una transformación global.** Una farola y una sombra profunda en la misma foto comparten la misma curva, y puede quemar las zonas de luz.
- **Puede dar un aspecto poco natural**, con contraste exagerado y bandas visibles.

Una posible mejora para proponer en la discusión es la **ecualización adaptativa (CLAHE)**: ecualiza por regiones y limita cuánto puede crecer el contraste. Otra opción es suavizar o promediar antes de ecualizar, enlazando con las operaciones aritméticas o con el tema de ruido.

---

Para comprobar que lo tienes, una pregunta: si aplicas la ecualización **dos veces seguidas** a la misma imagen, ¿qué esperas que pase con el resultado? Piénsalo con el ejemplo de la tabla.
