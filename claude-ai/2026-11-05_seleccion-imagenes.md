# Selección aleatoria de las imágenes

| | |
|---|---|
| Herramienta | Claude en claude.ai (proyecto de la asignatura) |
| Modelo | no consta en el export |
| Inicio | 2026-11-05 11:34 CET |
| Fin | 2026-11-05 11:58 CET |
| Conversación | `fc2d4aaf-b7e8-4342-b469-e44cb2ba2b08` |
| Mensajes del autor | 5 |
| Llamadas a herramientas | Projects ×2, memory_read ×1 |

> Transcripción generada con `scripts/exportar_sesiones.py` a partir del export de la cuenta de claude.ai. Se reproducen completos los mensajes del autor y los textos de respuesta de Claude; las llamadas a herramientas se resumen en una línea y se omiten sus resultados, el contenido de los adjuntos y el razonamiento interno del modelo.

---

## Mensaje 1 · 11:34

**Autor:**

> Y si elijo las fotos al azar?

**Claude:**

- `[Memoria] va-actividad-1.md`
- `[Proyecto] project_search «actividad 1 enunciado selección de imágenes criterios»`
- `[Proyecto] project_search «justificar la selección de las cuatro imágenes material y métodos características»`

Puedes, pero tal cual no te conviene, por dos motivos que salen del propio enunciado:

1. **Tienes que justificar cada decisión.** La sección de Material y métodos pide justificar todas las decisiones metodológicas, y "las elegí al azar" es una justificación pobre si luego no aporta nada al análisis.
2. **Las conclusiones piden comparar.** Se espera que digas qué técnicas funcionan mejor *según la imagen*. Con 4 fotos al azar de Dark Face es fácil que te salgan cuatro casi iguales (todo muy oscuro y uniforme). Entonces la comparación queda plana: la ecualización, el gamma y el log harán lo mismo en las cuatro.

**Lo que sí funciona bien es un término medio.** Usas el azar para no sesgar la búsqueda y después eliges con un criterio que puedes defender:

- Sacas una muestra aleatoria de candidatas, por ejemplo 30, con una **semilla fija**. Así otra persona puede repetir tu selección exacta, y eso suma en "replicabilidad".
- Calculas a cada una un par de indicadores sencillos: intensidad media (lo oscura que es), desviación típica (contraste) y porcentaje de píxeles saturados (farolas, faros…).
- Escoges 4 que cubran casos distintos. Por ejemplo:
  - una muy oscura y de bajo contraste,
  - una oscura con fuentes de luz intensas (aquí la ecualización global sufre y el log o el gamma brillan),
  - una con algo más de luz pero contraste comprimido,
  - una con mucho ruido visible.

Un esqueleto para empezar, para que lo completes tú:

```python
import cv2, numpy as np, random, glob

random.seed(42)
rutas = random.sample(sorted(glob.glob("DarkFace/*.png")), 30)

for r in rutas:
    g = cv2.imread(r, cv2.IMREAD_GRAYSCALE)
    media, std = g.mean(), g.std()
    sat = (g >= 250).mean() * 100
    print(f"{r}  media={media:.1f}  std={std:.1f}  saturados={sat:.2f}%")
```

Mira la extensión real de los archivos de tu copia del dataset y ajusta el `glob`. Esa tabla de indicadores te sirve además dos veces en la memoria: en Métodos justifica la selección, y en Resultados es tu línea base para el "antes y después".

Un apunte: en un dataset nocturno, una media de ~10–30 sobre 255 es lo normal. No descartes una imagen por parecer "negra" en el visor, porque esas son justo las que mejor lucen tras el realce.

¿Tienes ya el dataset descargado? Si quieres, pásame la salida de ese script y vemos juntos qué cuatro elegir.

---

## Mensaje 2 · 11:43

**Autor:**

> *[Fichero adjunto: `resultados.txt`]*

**Claude:**

Buena muestra. Que hayas sacado 100 en vez de 30 no es problema: anota en la memoria la semilla y el tamaño de la muestra, y listo.

**Lo primero que se ve:** el rango es enorme. La media va de 0.1 a 45.5, así que tienes material de sobra para elegir casos distintos. Te propongo una preselección, con dos o tres candidatas por categoría para que decidas tú mirándolas:

| Caso | Candidatas | Por qué |
|---|---|---|
| Muy oscura, bajo contraste | **182** (3.0 / 8.3), 2027 (2.9 / 8.3), 1711 (0.9 / 5.9) | Histograma apelotonado cerca de 0: el caso típico para gamma, log y ecualización |
| Oscura con focos de luz | **5069** (10.3 / 23.8 / 0.40 %), 2713 (8.5 / 27.2 / 0.22 %) | Fondo oscuro con focos saturados. Aquí la ecualización global y el estiramiento lineal suelen fallar, y eso te da discusión |
| Más luz pero contraste comprimido | **5940** (39.0 / 36.6 / 0.01 %), 672 (45.5 / 39.9) | La desviación típica es baja para su media. Es buena candidata para el estiramiento lineal |
| Ruidosa | sin determinar | Tu tabla no mide ruido, ver abajo |

Hay un caso extremo que puede darte un buen apartado de **limitaciones**: 3665 (0.1 / 1.1) o 2416 (0.3 / 1.3). Están tan oscuras que casi toda la información cabe en 2 o 3 niveles de gris. Al realzarlas aparecerán bandas (*posterización*) y ruido amplificado. Esto conecta directamente con el tema 3 de cuantificación, porque ningún realce puede recuperar niveles que nunca se capturaron. Puedes comprobarlo con `len(np.unique(g))`.

**Tres cosas que hacer antes de decidir:**

1. **Mira las imágenes.** Los números no te dicen qué contienen. Descarta las que no tengan nada reconocible (caras, edificios, una calle), porque el "antes y después" luce mucho más con contenido.
2. **Mide el ruido** para cubrir la cuarta categoría. Un estimador sencillo es la diferencia con una versión filtrada por mediana:
   ```python
   ruido = np.std(g.astype(float) - cv2.medianBlur(g, 3).astype(float))
   ```
   Añádelo a tu script y ordena por esa columna.
3. **Revisa el umbral de saturación.** Ninguna pasa del 0.5 %, porque las farolas ocupan muy pocos píxeles. Prueba con `>= 240` o mira `g.max()`, y comprueba visualmente que 5069 tiene de verdad focos de luz.

Mi apuesta inicial sería **182, 5069, 5940 y una ruidosa**, que puede salir del paso 2, o 3665 si prefieres el caso límite. Pero la última palabra la tiene lo que veas al abrirlas. ¿Me pasas la tabla con la columna de ruido cuando la tengas?

---

## Mensaje 3 · 11:49

**Autor:**

> Como ruidosa he escogido la 81

**Claude:**

Ojo con una cosa: **la 81 no está en tu muestra de 100**. Si en la memoria cuentas que seleccionaste a partir de una muestra aleatoria con semilla fija, una imagen de fuera rompe ese relato, y quien intente replicarlo no llegará a ella.

Tienes dos salidas, las dos válidas:

1. **Buscar la ruidosa dentro de la muestra.** Añades la columna de ruido al script, ordenas y eliges la que más destaque tras mirarla. El procedimiento queda limpio de principio a fin.
2. **Quedarte con la 81 y declararlo.** Por ejemplo: "tres imágenes se seleccionaron de una muestra aleatoria (semilla 42, n = 100) según media, contraste y saturación; la cuarta se añadió manualmente por presentar un nivel de ruido visiblemente superior, al no estar representado ese caso en la muestra". Para que esto se sostenga, conviene que calcules el estimador de ruido para la 81 y para las 100. Así puedes demostrar con un número que realmente es más ruidosa que cualquiera de la muestra.

Yo iría por la 2 si la 81 te gusta por su contenido. Haz la comparación numérica, porque si alguna de las 100 sale igual de ruidosa, lo honesto es usar esa.

¿Cómo llegaste a la 81? ¿La viste hojeando el dataset?

---

## Mensaje 4 · 11:56

**Autor:**

> import cv2, numpy as np, random, glob
>
> random.seed(42)
> rutas = random.sample(sorted(glob.glob("imgs/*.png")), 100)
> rutas = rutas.append("imgs/81.png")
>
> for r in rutas:
>     g = cv2.imread(r, cv2.IMREAD_GRAYSCALE)
>     media, std = g.mean(), g.std()
>     sat = (g >= 250).mean() * 100
>     ruido = np.std(g.astype(float) - cv2.medianBlur(g, 3).astype(float))
>     print(f"{r}  media={media:.1f}  std={std:.1f}  saturados={sat:.2f}% ruido={ruido:.2f}")
>
> me dice que ruta no es iterabel

**Claude:**

El error está en esta línea:

```python
rutas = rutas.append("imgs/81.png")
```

`append` modifica la lista directamente y **devuelve `None`**. Al asignar ese resultado a `rutas`, la lista se pierde y `rutas` pasa a valer `None`, que no se puede iterar. Quita la asignación:

```python
rutas.append("imgs/81.png")
```

El resto del script está bien. Como añades la 81 después de `random.sample`, la muestra de 100 sigue siendo exactamente la misma que antes con la semilla 42, y no rompes la reproducibilidad.

Cuando lo ejecutes, fíjate en dos cosas:

- **El ruido de la 81 frente a los 100.** Si queda por encima de todas, tienes tu justificación numérica.
- **Ruido en relación con el brillo.** En imágenes muy oscuras el estimador sale bajo simplemente porque hay poca señal, así que comparar valores absolutos puede engañar. Si ves que las imágenes más oscuras salen todas con poco ruido, prueba también con `ruido / std`.

Pásame la salida y elegimos.

---

## Mensaje 5 · 11:57

**Autor:**

> *[Fichero adjunto: `resultados.txt`]*

**Claude:**

Ahí está la respuesta: **la 5019 está dentro de tu muestra y es igual de ruidosa que la 81** (10.97 frente a 10.79). Las dos además tienen un brillo parecido (13.4 frente a 12.4). El resto de las 100 no pasa de 5.5, así que esas dos son claramente atípicas, con el doble de ruido que cualquier otra.

Con esto, la 81 ya no aporta nada que la muestra no tenga, y meterla te obliga a justificar una excepción en el procedimiento. **Quédate con la 5019** y el proceso queda limpio de principio a fin. La única razón para mantener la 81 sería que su contenido fuera mucho mejor visualmente. Ábrelas las dos y compruébalo. De paso confirma que ese "ruido" es grano de sensor y no artefactos de compresión, porque dos valores tan separados del resto merecen un vistazo.

Tu selección quedaría así:

| Imagen | Caso | Media | Std | Saturados | Ruido |
|---|---|---|---|---|---|
| 182 | Muy oscura, bajo contraste | 3.0 | 8.3 | 0.00 % | 1.91 |
| 5069 | Oscura con focos de luz | 10.3 | 23.8 | 0.40 % | 2.36 |
| 5940 | Más luz, contraste comprimido | 39.0 | 36.6 | 0.01 % | 5.48 |
| 5019 | Ruidosa | 13.4 | 29.5 | 0.03 % | 10.97 |

Esta tabla va casi tal cual a Material y métodos como justificación de la selección. Después la reutilizas en Resultados como línea base para el "antes y después", porque repetirás estas mismas métricas sobre las imágenes procesadas.

**Siguiente paso:** aplicar las técnicas del tema 6 a las cuatro (negativo, estiramiento lineal y no lineal, log, gamma, ecualización y operaciones aritméticas), guardando histogramas y métricas de cada resultado. ¿Empezamos montando la estructura del script para que procese las cuatro de una vez?
