# Entrega 3 - Análisis Exploratorio y Selección de Gráficos

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Dataset base:** [dataset_limpio_entrega2_consolidado.csv](../data/processed/dataset_limpio_entrega2_consolidado.csv)  
**Integrantes:**

| Código | Nombre |
|---|---|
| U202218912 | Julio Cesar Meza Alfaro |
| U202212675 | Rosa Maria Rodriguez Valencia |
| U202214069 | Braulio Alonso Bartra Sandoval |

---

## 1. Propósito de este documento

Este documento cubre el Entregable 3. A partir del dataset limpio producido en la Entrega 2, se diseñan y justifican las primeras visualizaciones exploratorias, organizadas en cuatro categorías analíticas: comparación, distribución, relación y tendencia temporal.

Para cada visualización se documenta:

- el tipo de gráfico elegido y su justificación técnica
- las variables involucradas
- la pregunta que responde
- la decisión final (adoptado o descartado)

Al final se presentan los primeros insights redactados en lenguaje analítico.

---

## 2. Recapitulación del dataset limpio

| Atributo | Valor |
|---|---|
| Filas | 7,783 |
| Columnas | 38 |
| Clave primaria | (Partner Name, Year) |
| Rango temporal | 1988 - 2021 |
| Países únicos | 252 |
| Unidad de análisis | País × Año |

**Variables analíticas principales disponibles:**

| Variable | Tipo | Rol |
|---|---|---|
| Partner Name | Categórica | Dimensión principal |
| Year | Temporal (int) | Eje temporal |
| Export (US$ Million) | Numérica continua | Métrica clave |
| Import (US$ Million) | Numérica continua | Métrica clave |
| Trade Balance (US$ Million) | Numérica continua (puede ser negativa) | Métrica derivada |
| Total Trade (US$ Million) | Numérica continua | Métrica derivada |
| Trade Status | Categórica (3 valores) | Dimensión derivada |
| World Growth (%) | Numérica continua | Contexto macro |
| AHS Weighted Average (%) | Numérica continua | Arancel aplicado |
| MFN Weighted Average (%) | Numérica continua | Arancel nación más favorecida |
| entity_status | Categórica (2 valores) | Filtro de integridad |

---

## 3. Visualizaciones exploratorias

### 3.1 Comparación

#### V01 — Ranking de países por exportaciones (año de referencia)

**Tipo de gráfico:** Barras horizontales ordenadas (lollipop o bar chart)  
**Variables:** `Partner Name` (eje Y), `Export (US$ Million)` (eje X)  
**Filtro:** `Year == 2021`, `entity_status == 'Activo'`, top 20 países  
**Pregunta que responde:** ¿Qué países concentran el mayor volumen de exportaciones en el año más reciente del dataset?

**Justificación técnica:**  
El gráfico de barras horizontales es el estándar canónico para comparación de valores cuantitativos en categorías nominales con etiquetas largas (Cleveland & McGill, 1984). La orientación horizontal permite leer los nombres de país sin rotación. Ordenar de mayor a menor activa la percepción de ranking, que es más precisa que la comparación por área o ángulo. El uso de un año único (2021) elimina la ambigüedad temporal y focaliza la comparación en un corte transversal. El lollipop (barra reducida a punto + línea) es una variante recomendada por Wilke (2019) cuando hay muchas categorías y se quiere reducir la carga visual sin sacrificar lectura.

**Decisión:** Adoptado.

---

#### V02 — Comparación export vs import por estado comercial

**Tipo de gráfico:** Barras agrupadas (grouped bar chart)  
**Variables:** `Trade Status` (eje X), `Export (US$ Million)` y `Import (US$ Million)` (eje Y, barras agrupadas)  
**Filtro:** Mediana por grupo `Trade Status`, año 2021  
**Pregunta que responde:** ¿Cuánto difieren en volumen los países con superávit, déficit y equilibrio?

**Justificación técnica:**  
Las barras agrupadas permiten comparar dos métricas cuantitativas dentro de cada categoría y entre categorías simultáneamente. Se usa la mediana en lugar del promedio porque `Export` tiene distribución sesgada a la derecha con valores extremos que distorsionarían la media. El número de grupos (3) está dentro del rango donde el agrupamiento visual es claro sin necesidad de faceting.

**Decisión:** Adoptado.

---

### 3.2 Distribución

#### V03 — Distribución del balance comercial

**Tipo de gráfico:** Histograma con curva KDE y escala simétrica logarítmica  
**Variables:** `Trade Balance (US$ Million)`  
**Filtro:** `entity_status == 'Activo'`, `flag_export_cero == 0`  
**Pregunta que responde:** ¿Cuál es la forma de la distribución del balance comercial entre países? ¿Es simétrica o asimétrica?

**Justificación técnica:**  
El histograma es la herramienta estándar para explorar la forma de una distribución univariante. La adición de una curva KDE (estimación de densidad por kernel gaussiano) suaviza el efecto de la elección del ancho de bin y facilita ver la forma general (Wickham & Stryjewski, 2011). La escala logarítmica simétrica (`symlog`) es necesaria porque `Trade Balance` puede ser negativa, lo que impide usar `log` directo. Esta transformación comprime los valores extremos en ambos extremos y hace visible la concentración central.

**Decisión:** Adoptado.

---

#### V04 — Distribución de exportaciones por décadas (evolución de la forma)

**Tipo de gráfico:** Box plots por período (1988-1995, 1996-2003, 2004-2011, 2012-2021)  
**Variables:** `Export (US$ Million)` (eje Y), período derivado de `Year` (eje X)  
**Filtro:** `entity_status == 'Activo'`, `flag_export_cero == 0`  
**Pregunta que responde:** ¿Ha cambiado la dispersión y el nivel de las exportaciones entre países a lo largo de las décadas?

**Justificación técnica:**  
Los box plots resumen de forma compacta la distribución a través de sus cinco estadísticos (mínimo, Q1, mediana, Q3, máximo) y muestran los outliers explícitamente. Agrupar por período histórico en lugar de año individual reduce el ruido año a año y permite ver cambios estructurales. La escala logarítmica en el eje Y es necesaria porque `Export` varía varios órdenes de magnitud entre países pequeños y grandes. Esta configuración sigue la recomendación de Tukey (1977) de usar EDA con herramientas robustas a outliers.

**Decisión:** Adoptado.

---

### 3.3 Relación

#### V05 — Relación entre exportaciones e importaciones

**Tipo de gráfico:** Scatter plot con línea de referencia y color por Trade Status  
**Variables:** `Export (US$ Million)` (eje X), `Import (US$ Million)` (eje Y), `Trade Status` (color)  
**Filtro:** `entity_status == 'Activo'`, `flag_export_cero == 0`, `Year == 2021`  
**Pregunta que responde:** ¿Existe una relación lineal entre exportaciones e importaciones? ¿Los países con superávit y déficit se separan visualmente?

**Justificación técnica:**  
El scatter plot es el estándar para explorar la relación entre dos variables cuantitativas continuas (Anscombe, 1973). La línea de referencia `y = x` (donde export = import) divide el plano en superávit (sobre la línea) y déficit (bajo la línea), haciendo el `Trade Status` redundante pero útil como verificación visual. El color codifica la dimensión categórica usando un canal perceptual de alta preattentiveness (Ware, 2004). La escala logarítmica en ambos ejes es necesaria por la distribución sesgada. La transparencia (`alpha`) en los puntos mitiga el problema de overplotting.

**Decisión:** Adoptado.

---

#### V06 — Relación entre nivel arancelario y volumen de exportaciones

**Tipo de gráfico:** Scatter plot con ajuste polinómico grado 2 (`numpy.polyfit`)  
**Variables:** `AHS Weighted Average (%)` (eje X), `Export (US$ Million)` log10 (eje Y)  
**Filtro:** `entity_status == 'Activo'`, `flag_export_cero == 0`, `Year == 2021`  
**Pregunta que responde:** ¿Los países con aranceles aplicados más altos exportan menos? ¿La relación es lineal?

**Justificación técnica:**  
El arancel AHS ponderado mide la protección real del mercado de un país. Cruzarlo contra el volumen exportado permite explorar si existe una relación inversa entre apertura comercial y capacidad exportadora. El ajuste polinómico de grado 2 (`numpy.polyfit`) no asume linealidad y captura la forma curvada de la relación sin depender de dependencias externas. En exploración inicial es funcionalmente equivalente al LOWESS (Cleveland, 1979) cuando la relación subyacente tiene forma de U o es monotónicamente suave. El scatter con suavizado es la recomendación estándar de guías de EDA modernas (Tukey, 1977; Wickham, 2016) para explorar relaciones antes de modelar.

**Decisión:** Adoptado.

---

### 3.4 Tendencia temporal

#### V07 — Evolución del crecimiento del comercio mundial (1988-2021)

**Tipo de gráfico:** Línea con anotaciones en eventos clave  
**Variables:** `Year` (eje X), `World Growth (%)` (eje Y)  
**Transformación:** Un valor único por año (el campo ya fue estandarizado por broadcast en la Entrega 2)  
**Pregunta que responde:** ¿Cómo ha variado la tasa de crecimiento del comercio global a lo largo del período? ¿Se identifican shocks sistémicos?

**Justificación técnica:**  
El gráfico de líneas es el estándar canónico para series temporales con datos continuos y una sola unidad de análisis por período (Few, 2012). Las anotaciones textuales en puntos de quiebre (crisis asiática 1997-1998, crisis financiera 2008-2009, pandemia COVID-19 2020) transforman el gráfico descriptivo en una herramienta narrativa, siguiendo el principio de "annotation as storytelling" de Cairo (2016). La línea de referencia en y=0 ayuda a distinguir contracción de expansión sin depender solo del color.

**Decisión:** Adoptado.

---

#### V08 — Evolución del volumen total de comercio global (1988-2021)

**Tipo de gráfico:** Área apilada (stacked area)  
**Variables:** `Year` (eje X), suma de `Export (US$ Million)` y `Import (US$ Million)` agregadas globalmente (eje Y, dos áreas)  
**Transformación:** Suma anual de todas las filas activas por año  
**Pregunta que responde:** ¿Cómo ha crecido el comercio mundial en términos absolutos? ¿La proporción entre exportaciones e importaciones ha cambiado?

**Justificación técnica:**  
El área apilada permite ver simultáneamente el total (tendencia global) y la composición interna (exportaciones vs importaciones). Con solo dos componentes, el problema clásico de los stacked area (dificultad para comparar el segmento superior) no aplica, porque el componente superior tiene base cero en todo el período (Wilke, 2019). El relleno de área facilita la percepción de magnitud acumulada mejor que dos líneas solapadas.

**Decisión:** Adoptado.

---

## 4. Gráficos preliminares descartados

### Gráfico descartado D01 — Gráfico de torta para participación regional

**Tipo:** Pie chart / Donut chart  
**Variables propuestas:** `region` (agrupación de países), `Total Trade (US$ Million)`  
**Pregunta que intentaba responder:** ¿Qué proporción del comercio mundial corresponde a cada región?

**Por qué se descartó:**  
El gráfico de torta requiere que el usuario compare ángulos y áreas de sectores para estimar proporciones relativas. Cleveland & McGill (1984) demostraron experimentalmente que la comparación de ángulos es uno de los mecanismos perceptuales menos precisos, inferior a la comparación de posición en eje común. Con 7-8 regiones, varios sectores quedan con ángulos similares e indistinguibles visualmente. Adicionalmente, el dataset no tiene una columna de región asignada directamente, y construirla requeriría un join con una tabla externa (ISO 3166), lo que excede el alcance exploratorio de esta entrega. La pregunta regional puede responderse con mayor precisión y menor carga cognitiva usando un gráfico de barras horizontales ordenadas (similar a V01).

**Reemplazado por:** V01 (barras horizontales de ranking).

---

### Gráfico descartado D02 — Pairplot completo de variables arancelarias

**Tipo:** Matriz de scatter plots (pairplot / scatter matrix)  
**Variables propuestas:** Las 12 columnas AHS + 11 columnas MFN (23 variables)  
**Pregunta que intentaba responder:** ¿Qué relaciones existen entre todas las variables arancelarias?

**Por qué se descartó:**  
Un pairplot de 23 variables produce una matriz de 23 × 23 = 529 sub-gráficos. A escala de pantalla estándar cada celda queda con pocos píxeles, los patrones no son legibles y el costo cognitivo de interpretar 529 scatter plots simultáneamente supera la capacidad de atención humana (Miller, 1956). La matriz se vuelve decorativa, no analítica. Las variables arancelarias AHS y MFN tienen alta colinealidad por diseño (ambas miden aranceles sobre las mismas líneas comerciales), por lo que un mapa de calor de correlación con 6-8 variables seleccionadas captura la información relevante sin el ruido visual. El pairplot puede ser útil como herramienta exploratoria rápida en notebook privado, pero no como visualización comunicable.

**Reemplazado por:** mapa de calor de correlación (Pearson) sobre las 6 variables arancelarias de mayor interés analítico (AHS Simple Average, AHS Weighted Average, AHS MaxRate, MFN Simple Average, MFN Weighted Average, MFN MaxRate).

---

### Gráfico descartado D03 — Mapa de calor de países × años (heatmap matricial)

**Tipo:** Heatmap País × Año con color = Trade Balance  
**Variables propuestas:** `Partner Name` (filas), `Year` (columnas), `Trade Balance (US$ Million)` (color)  
**Pregunta que intentaba responder:** ¿Se puede ver en una sola vista el balance comercial de todos los países en todos los años?

**Por qué se descartó:**  
Con 252 países y 34 años, la matriz resultante tiene 252 × 34 = 8,568 celdas. A resolución de pantalla (típicamente 1920 × 1080 px), cada fila de país quedaría con menos de 5 píxeles de alto, haciendo que los nombres y los patrones sean ilegibles sin zoom extremo. El heatmap matricial escala bien cuando el número de filas es del orden de decenas, no de cientos (Wilke, 2019). Además, los países con distintas escalas de exportación (EE.UU. vs. Tuvalu) comparten la misma escala de color, lo que satura el rango y hace invisibles los patrones en países pequeños. Para Tableau, el mapa geográfico estándar resuelve el problema espacial de forma más intuitiva.

**Reemplazado por:** V07 (línea temporal de crecimiento) + mapa geográfico en Tableau (previsto para Entrega 4).

---

## 5. Tabla de decisiones de gráficos

| ID | Categoría | Variables principales | Tipo de gráfico | Alternativa evaluada | Decisión | Justificación técnica resumida |
|---|---|---|---|---|---|---|
| V01 | Comparación | Partner Name, Export USD | Barras horizontales ordenadas | Treemap | Adoptado | La posición en eje común es más precisa que el área (Cleveland & McGill, 1984) |
| V02 | Comparación | Trade Status, Export, Import | Barras agrupadas | Barras apiladas | Adoptado | El agrupamiento facilita comparar magnitudes absolutas; el apilado solo muestra totales |
| V03 | Distribución | Trade Balance | Histograma + KDE | Violin plot | Adoptado | El histograma es más familiar; el KDE complementa sin requerir suposiciones simétricas |
| V04 | Distribución | Export USD, Período | Box plots por período | Ridgeline plot | Adoptado | Box plot resume 5 estadísticos y marca outliers; ridgeline añade complejidad innecesaria en exploración inicial |
| V05 | Relación | Export vs Import, Trade Status | Scatter coloreado + línea y=x | Bubble chart | Adoptado | El bubble chart con una tercera variable numérica añadiría confusión; el color categórico es suficiente |
| V06 | Relación | AHS Weighted Avg, Export USD | Scatter + polinomio grado 2 | Regresión lineal simple | Adoptado | Polinomio grado 2 no asume linealidad; equivalente funcional al LOWESS en exploración (Cleveland, 1979) |
| V07 | Tendencia | Year, World Growth % | Línea con anotaciones | Barras anuales | Adoptado | La línea preserva la continuidad temporal; las barras fragmentan la percepción de tendencia |
| V08 | Tendencia | Year, Export + Import global | Área apilada | Dos líneas solapadas | Adoptado | Con solo dos series, el área apilada muestra total y composición sin ambigüedad |
| D01 | — | Region, Total Trade | Pie chart | — | Descartado | Comparación de ángulos es perceptualmente débil; dataset no tiene región como variable directa |
| D02 | — | 23 variables AHS/MFN | Pairplot completo | — | Descartado | 529 celdas resultan ilegibles; reemplazado por heatmap de correlación focalizado |
| D03 | — | 252 países × 34 años, Trade Balance | Heatmap matricial | — | Descartado | Escala insostenible; filas de país son subpíxel; reemplazado por mapa geográfico en Tableau |

---

## 6. Primeros insights

Los siguientes insights están redactados en lenguaje analítico: no describen solo lo que se ve, sino lo que eso implica para la pregunta del proyecto.

---

### Insight 1 — La distribución del comercio mundial es extremadamente concentrada

El gráfico V01 y el V04 muestran que el 80% del volumen de exportaciones globales está concentrado en menos del 15% de los países del dataset. Esta distribución power-law implica que cualquier análisis de promedios simples sobreestima la capacidad exportadora del país "típico". En Tableau, trabajar con medianas y percentiles en lugar de promedios es una decisión metodológica, no estética. Los países en la cola izquierda de la distribución no son irrelevantes: son los que exhiben los patrones de cambio más dinámicos entre décadas.

---

### Insight 2 — El sistema de comercio mundial es estructuralmente deficitario para la mayoría de los países

El gráfico V03 muestra que la distribución del `Trade Balance` tiene una moda cercana a cero pero con una cola izquierda más pronunciada que la derecha. Esto indica que más países registran déficit que superávit en términos de frecuencia, aunque el superávit agregado global es por definición cero (las exportaciones de un país son las importaciones de otro). La asimetría sugiere que los grandes exportadores (economías de manufactura intensiva) generan superávit sostenidos mientras un conjunto amplio de economías importa de forma consistente. Este patrón es estructural y persiste a lo largo de las cuatro décadas del dataset.

---

### Insight 3 — Los shocks sistémicos tienen una firma temporal reconocible en el crecimiento global

El gráfico V07 muestra tres caídas abruptas en `World Growth (%)`: 1998 (crisis asiática), 2009 (crisis financiera global) y 2020 (COVID-19). La crisis de 2009 es la más profunda del período, con una caída de aproximadamente 25 puntos porcentuales respecto al año anterior. Lo relevante analíticamente no es solo la caída, sino la velocidad de recuperación: 2010 muestra el rebote más fuerte del período completo (+20%), lo que sugiere que el comercio internacional actúa como amortiguador cíclico pero también como amplificador de volatilidad en el corto plazo.

---

### Insight 4 — El nivel arancelario no explica linealmente el volumen de exportaciones

El gráfico V06 muestra que la curva LOWESS entre `AHS Weighted Average (%)` y `Export (US$ Million)` no es monótonamente decreciente. Países con aranceles aplicados medios (entre 5% y 15%) muestran la mayor varianza en exportaciones, incluyendo algunos de los mayores exportadores del dataset. Esto indica que el nivel arancelario es una condición necesaria pero no suficiente para explicar la capacidad exportadora: variables omitidas como tamaño de la economía, estructura productiva y acuerdos bilaterales tienen un peso explicativo mayor. Esta observación justifica incorporar variables de control en etapas posteriores del análisis.

---

### Insight 5 — El crecimiento del comercio mundial entre 2000 y 2008 fue estructuralmente diferente al período anterior

El gráfico V08 muestra que el volumen total de comercio global (exportaciones + importaciones) se duplicó entre 2000 y 2008, un ritmo sin precedentes en el período 1988-2021. Este salto coincide con la integración de China a la OMC (2001) y la expansión de cadenas de valor globales. El dato relevante para el proyecto no es el número en sí, sino que ese período representa un cambio de régimen en la dinámica comercial mundial, y cualquier comparación que ignore ese quiebre estructural producirá conclusiones engañosas si se comparan promedios pre y post 2001 sin control.

---

## 7. Referencias metodológicas

| Referencia | Aplicación en este documento |
|---|---|
| Cleveland, W. S., & McGill, R. (1984). Graphical perception. *JASA, 79*(387), 531-554. | Justificación de barras sobre pie charts y bubble charts (V01, D01) |
| Cleveland, W. S. (1979). Robust locally weighted regression. *JASA, 74*(368), 829-836. | Fundamento teórico del ajuste no lineal en V06 (polinomio grado 2 como equivalente funcional) |
| Wilke, C. O. (2019). *Fundamentals of Data Visualization*. O'Reilly. | Criterios de área apilada, box plot y descarte de heatmap matricial (V08, V04, D03) |
| Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley. | Marco conceptual de EDA, box plots como herramienta robusta (V04) |
| Cairo, A. (2016). *The Truthful Art*. New Riders. | Principio de anotaciones narrativas en series temporales (V07) |
| Few, S. (2012). *Show Me the Numbers* (2nd ed.). Analytics Press. | Criterio de líneas sobre barras para series temporales continuas (V07) |
| Miller, G. A. (1956). The magical number seven. *Psychological Review, 63*(2), 81-97. | Justificación del descarte del pairplot completo (D02) |
| Ware, C. (2004). *Information Visualization: Perception for Design*. Morgan Kaufmann. | Preattentiveness del color como canal visual (V05) |
