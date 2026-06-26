# Entrega 4 — Explicación Completa y Cumplimiento de Requisitos

## Proyecto

**Curso:** Data Visualization (1ACC0211) — UPC  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1988-2021)  

| Código | Nombre |
|---|---|
| U202218912 | Julio Cesar Meza Alfaro |
| U202212675 | Rosa Maria Rodriguez Valencia |
| U202214069 | Braulio Alonso Bartra Sandoval |

---

## Propósito de este documento

Este documento explica de manera completa **qué se hizo en la Entrega 4, por qué se hizo de esa manera, y en qué parte exacta de nuestros entregables se cumple cada requisito** exigido por la propuesta del trabajo final.

La idea es que una persona que no participó en el desarrollo pueda:

- entender qué contiene cada archivo generado
- verificar que cada criterio de la rúbrica está cubierto
- encontrar exactamente dónde está la evidencia de cada requisito

---

## Archivos generados en esta entrega

| Archivo | Tipo | Para qué sirve |
|---|---|---|
| [`notebooks/entrega4-calculos-segmentacion.ipynb`](../notebooks/entrega4-calculos-segmentacion.ipynb) | Notebook Jupyter | Contiene toda la lógica de segmentación, cálculos analíticos y exportación. Es el entregable principal de código. |
| [`docs/entrega4-reglas-segmentacion.md`](../docs/entrega4-reglas-segmentacion.md) | Documento Markdown | Documento breve de reglas de métricas, segmentos y parámetros. Es el entregable documental. |
| [`outputs/tableau_sources/Fact_Trade.csv`](../outputs/tableau_sources/Fact_Trade.csv) | CSV | Tabla de hechos enriquecida (9 columnas). Fuente final para Tableau. |
| [`outputs/tableau_sources/Dim_Country.csv`](../outputs/tableau_sources/Dim_Country.csv) | CSV | Dimensión de países con segmentación ABC incluida. Fuente final para Tableau. |
| [`outputs/tableau_sources/Dim_Time.csv`](../outputs/tableau_sources/Dim_Time.csv) | CSV | Dimensión temporal (sin cambios respecto a Entrega 3). Fuente final para Tableau. |
| [`outputs/tableau_sources/QA_Metricas_Derivadas.csv`](../outputs/tableau_sources/QA_Metricas_Derivadas.csv) | CSV | Tabla auxiliar de control de calidad. No es para Tableau, es para verificar que los cálculos en Tableau coincidan con los de Python. |
| [`scripts/entrega4_calculos.py`](../scripts/entrega4_calculos.py) | Script Python | Versión ejecutable de la misma lógica del notebook. Auxiliar de desarrollo, no es un entregable formal. |

---

## Qué se hizo paso a paso y por qué

### Paso 1 — Segmentación ABC de países por exportaciones

**Qué se hizo:**  
Se tomó el volumen total de exportaciones históricas (suma de 1988 a 2021) de cada uno de los 252 países del dataset. Se ordenaron de mayor a menor y se calculó la participación acumulada. Luego se clasificaron en tres segmentos (Tiers) usando el principio de Pareto:

| Tier | Criterio | Resultado |
|---|---|---|
| Tier 1 — Grandes Exportadores | Acumulan hasta el 80% del volumen global | 29 países (11.5%) → 79.5% del volumen |
| Tier 2 — Exportadores Medianos | Del 80% al 95% | 43 países (17.1%) → 15.4% del volumen |
| Tier 3 — Exportadores Pequeños | Del 95% al 100% | 180 países (71.4%) → 5.1% del volumen |

**Por qué se hizo así y no de otra manera:**

- *¿Por qué Pareto y no otra clasificación?* Porque en la Entrega 3 (Insight 1) ya se había demostrado empíricamente que la distribución de exportaciones sigue una distribución power-law (muy pocos países concentran casi todo). El principio de Pareto (80/20) es el criterio estándar para segmentar distribuciones de este tipo. No es arbitrario: responde a un hallazgo analítico previo del propio proyecto.

- *¿Por qué se usó el volumen total histórico (1988-2021) en vez del último año (2021)?* Porque 2021 fue un año atípico por el rebote post-COVID (el Insight 3 de la Entrega 3 mostró que 2020 tuvo una caída de -15% y 2021 un rebote agresivo). Si segmentáramos solo por 2021, estaríamos clasificando a los países por su capacidad de recuperación post-pandemia, no por su relevancia comercial estructural. El total histórico captura la relevancia sostenida a lo largo de 34 años.

- *¿Por qué se guardó el Tier en `Dim_Country` y no en `Fact_Trade`?* Porque el Tier es un atributo del país, no de la transacción. Un país es "Tier 1" independientemente del año. Si lo pusiéramos en la tabla de hechos, estaríamos repitiendo el mismo valor en cada fila del país (redundancia). En un Esquema en Estrella, los atributos descriptivos van en la dimensión, no en el fact.

**Dónde está la evidencia:**  
- Notebook: Sección 1, celdas de código con el cálculo y la tabla resumen.
- Documento de reglas: Sección 2, "Reglas de Segmentación: Export Tier (ABC)".

---

### Paso 2 — Enriquecimiento del Esquema en Estrella

**Qué se hizo:**  
La tabla de hechos (`Fact_Trade`) de la Entrega 3 solo contenía 3 columnas: `dim_time_sk`, `dim_country_sk`, y `Export (US$ Million)`. Se enriqueció a 9 columnas, trayendo del dataset limpio (Entrega 2) las siguientes métricas transaccionales:

- `Import (US$ Million)` — para calcular balance y comparaciones export vs import
- `Trade Balance (US$ Million)` — para análisis de superávit/déficit
- `Total Trade (US$ Million)` — para volumen total bilateral
- `Trade Status` — para segmentar por superávit/déficit/equilibrio
- `AHS Weighted Average (%)` — arancel aplicado ponderado
- `MFN Weighted Average (%)` — arancel nación más favorecida ponderado

**Por qué se hizo así y no de otra manera:**

- *¿Por qué no se trajo `World Growth (%)` al fact?* Porque ese fue exactamente el problema que la Entrega 3 identificó y resolvió con el Esquema en Estrella. `World Growth (%)` depende solo del año, no del país. Si lo ponemos en el fact, se repite 252 veces por año y un `AVG()` produce un promedio ponderado falso (fan-out trap). Se mantiene aislado en `Dim_Time` donde existe una sola fila por año.

- *¿Cómo se verificó que el join no rompió nada?* Se hizo un `assert` programático que verifica que el número de filas antes y después del merge es exactamente 7,783. Si hubiera sido diferente, significaría que el join produjo duplicados (fan-out) o perdió filas (inner join excluyendo datos). El assert pasó: el join fue 1:1.

- *¿Por qué estas métricas sí van en el fact y `World Growth` no?* Porque Import, Trade Balance, aranceles, etc. dependen de la combinación *país × año* (son transaccionales). Cada fila del fact tiene un valor distinto para cada país en cada año. En cambio, `World Growth` tiene el mismo valor para todos los países del mismo año — eso lo convierte en un atributo dimensional del año, no del hecho comercial.

**Dónde está la evidencia:**  
- Notebook: Sección 2, celda del paso 2.3 con el assert de verificación.
- Documento de reglas: Sección 1, "Por qué el Fact_Trade no contiene World Growth (%)".

---

### Paso 3 — Métricas derivadas (prototipado y QA en Python)

**Qué se hizo:**  
Se calcularon tres métricas derivadas en Pandas como valores de referencia:

| Métrica | Fórmula | Para qué sirve |
|---|---|---|
| **Variación Interanual (YoY %)** | `(Export_t − Export_{t-1}) / Export_{t-1} × 100` | Mide la dinámica de cambio: ¿un país está creciendo o decreciendo respecto al año anterior? |
| **Share of Global Exports (%)** | `Export_país / Total_mundial_año × 100` | Mide la participación relativa: ¿un país está ganando o perdiendo peso en el comercio global? |
| **Promedio Móvil 3 años** | `mean(Export_{t-2}, Export_{t-1}, Export_t)` | Suaviza la volatilidad interanual para ver tendencias de mediano plazo. |

**Por qué se hizo así y no de otra manera:**

- *¿Por qué calcular en Python si luego se va a hacer en Tableau?* Porque necesitamos un "ground truth" (verdad de referencia). Cuando repliquemos estos cálculos en Tableau con LODs o Table Calculations, necesitamos un archivo de control (`QA_Metricas_Derivadas.csv`) contra el cual comparar. Si los números de Tableau no coinciden, sabremos que el LOD está mal configurado. Esto es una práctica estándar de aseguramiento de calidad.

- *¿Por qué se eligieron estas tres métricas y no otras?* Porque responden directamente a la pregunta analítica del proyecto:
  - **YoY %** → captura la *dinámica* del comercio (no solo el nivel).
  - **Share %** → captura la *posición relativa* de un país (eliminando el efecto del crecimiento global).
  - **Promedio Móvil** → captura la *tendencia* suavizada (eliminando ruido de años atípicos como 2009 o 2020).
  - Juntas, cubren los tres ángulos que la propuesta exige bajo el tema "Cálculos analíticos": métricas derivadas, porcentajes o participaciones, y acumulados o comparaciones relativas.

- *¿Cómo se validó que el Share está bien calculado?* Se verificó programáticamente que la suma de Share de todos los países, para cada año, da exactamente 100.00%. Si un dato se hubiera perdido en algún join o filtro, la suma no daría 100%.

**Dónde está la evidencia:**  
- Notebook: Sección 3, celdas de cálculo y celda de validación QA.
- Documento de reglas: Sección 3, con las fórmulas, su equivalente en Tableau, y la explicación de "Cómo afecta la interpretación" para cada una.

---

### Paso 4 — Diseño de parámetros y lógica analítica para Tableau

**Qué se hizo:**  
Se diseñaron teóricamente (documentados, no implementados aún en Tableau) tres elementos de lógica analítica:

1. **Parámetro "Top N Países"** — un slider (5 a 50) que permite al usuario del dashboard filtrar dinámicamente cuántos países ver en rankings.
2. **LOD para Share** — `{FIXED [Year] : SUM([Export])}` que calcula el total mundial por año de forma independiente a los filtros de la vista.
3. **LOD para promedio por Tier** — `{FIXED [Export_Tier], [Year] : AVG([Export])}` que permite crear líneas de referencia por segmento.

**Por qué se hizo así y no de otra manera:**

- *¿Por qué un parámetro dinámico y no un filtro fijo de Top 10?* Porque un filtro fijo asume que el usuario final siempre quiere ver 10 países. Un parámetro delega esa decisión al usuario. Un ministro de economía puede querer ver solo los Top 5; un analista de investigación puede necesitar el Top 30. La interactividad tiene sentido analítico, no es decorativa.

- *¿Por qué LOD (`FIXED`) y no una Table Calculation (`% of Total`)?* Porque el LOD `{FIXED [Year]}` es inmune a los filtros de la vista. Si el usuario filtra por "Tier 1", la Table Calculation `% of Total` recalcularía el porcentaje solo sobre los países de Tier 1 (sumando 100% dentro del tier), lo cual es engañoso. El LOD mantiene el denominador como el total mundial real, sin importar los filtros aplicados.

- *¿Por qué estos diseños no se implementaron en Tableau todavía?* Porque la Entrega 4 pide explícitamente "parámetros o lógica analítica" y "fuentes para Tableau", no un dashboard. La implementación en Tableau corresponde a la Entrega 5 (Dashboard alpha). Implementarlos ahora sin las visualizaciones sería prematuro y no tendría forma de validarse visualmente.

**Dónde está la evidencia:**  
- Documento de reglas: Sección 4, "Parámetros y Lógica Analítica para Tableau".

---

### Paso 5 — Exportación de fuentes finales

**Qué se hizo:**  
Se exportaron los tres archivos CSV del Esquema en Estrella actualizados al directorio `outputs/tableau_sources/`:

| Archivo | Filas | Columnas | Cambio respecto a Entrega 3 |
|---|:---:|:---:|---|
| `Fact_Trade.csv` | 7,783 | 9 | +6 columnas (Import, Trade Balance, Total Trade, Trade Status, AHS, MFN) |
| `Dim_Country.csv` | 252 | 4 | +2 columnas (Export_Tier, Total_Export_Hist) |
| `Dim_Time.csv` | 34 | 3 | Sin cambios |
| `QA_Metricas_Derivadas.csv` | 7,783 | 8 | Nuevo (solo para QA, no para Tableau) |

**Por qué se hizo así y no de otra manera:**

- *¿Por qué se sobrescribieron los archivos de la Entrega 3?* Porque los nuevos archivos son un superset: contienen todo lo que tenían los anteriores más las columnas adicionales. No se eliminó ni se modificó ninguna columna existente. Cualquier workbook de Tableau que ya estuviera conectado a los archivos anteriores seguiría funcionando sin cambios.

- *¿Por qué el archivo de QA es separado y no va a Tableau?* Porque contiene columnas calculadas (YoY, Share, MA3) que en Tableau se deben calcular con Table Calculations o LODs para que sean dinámicas. Si las exportáramos como columnas estáticas en el CSV, perderían la capacidad de recalcularse cuando el usuario aplique filtros o cambie parámetros.

**Dónde está la evidencia:**  
- Notebook: Sección 4, celda de exportación con el listado de archivos y tamaños.
- Directorio `outputs/tableau_sources/` con los archivos generados.

---

## Cruce detallado con los requisitos de la propuesta

### A. Contenido exigido (líneas 357-363 de la propuesta)

| Contenido exigido | ¿Se cumple? | Dónde está |
|---|:---:|---|
| Estructura analítica o relacional para Tableau | ✓ | El Esquema en Estrella (Fact_Trade + Dim_Country + Dim_Time) con Relationships documentadas en el doc de reglas, Sección 1. |
| Métricas derivadas para visualización | ✓ | YoY %, Share %, Promedio Móvil 3 años. Calculadas en el notebook (Sección 3) y documentadas en el doc de reglas (Sección 3). |
| Segmentación | ✓ | Segmentación ABC en 3 Tiers (Pareto). Implementada en el notebook (Sección 1) y documentada en el doc de reglas (Sección 2). |
| Parámetros o lógica analítica | ✓ | Parámetro Top N, LOD Share, LOD Promedio por Tier. Diseñados en el doc de reglas (Sección 4). |
| Fuentes finales o semidefinitivas para Tableau | ✓ | Tres CSVs en `outputs/tableau_sources/`. Exportados en el notebook (Sección 4). |

---

### B. Entregables exigidos (líneas 365-369 de la propuesta)

| Entregable exigido | ¿Se cumple? | Archivo |
|---|:---:|---|
| Notebook de cálculos analíticos | ✓ | [`notebooks/entrega4-calculos-segmentacion.ipynb`](../notebooks/entrega4-calculos-segmentacion.ipynb) |
| Fuentes finales o semidefinitivas para Tableau | ✓ | [`outputs/tableau_sources/`](../outputs/tableau_sources/) — 3 CSVs listos para conectar |
| Documento breve de reglas de métricas, segmentos y parámetros | ✓ | [`docs/entrega4-reglas-segmentacion.md`](../docs/entrega4-reglas-segmentacion.md) |

---

### C. Criterios mínimos de aprobación (líneas 371-377 de la propuesta)

| Criterio | ¿Se cumple? | Evidencia concreta |
|---|:---:|---|
| **La estructura relacional está validada y no duplica métricas sin control** | ✓ | `World Growth (%)` se mantiene exclusivamente en `Dim_Time` (no en `Fact_Trade`), evitando el fan-out trap demostrado en la Entrega 3. El join de enriquecimiento se verificó con un `assert` que confirma 7,783 filas antes y después (sin duplicación). Ver notebook, Sección 2. |
| **Se implementan métricas derivadas consistentes con la pregunta del proyecto** | ✓ | Las tres métricas (YoY, Share, MA3) responden directamente a la pregunta del proyecto sobre la dinámica del comercio mundial. Ver notebook, Sección 3 y doc de reglas, Sección 3. |
| **Se define al menos un segmento relevante para el análisis posterior en Tableau** | ✓ | Segmentación ABC con 3 Tiers basada en Pareto. 252 países clasificados, 0 sin asignar. La columna `Export_Tier` está en `Dim_Country.csv`, lista para usar como filtro o dimensión en Tableau. Ver notebook, Sección 1. |
| **El equipo puede explicar cómo cada cálculo afecta la interpretación** | ✓ | Cada métrica y cada segmento tiene una sección "Cómo afecta la interpretación" en el doc de reglas (Secciones 2 y 3). Cada celda de código del notebook tiene una celda Markdown precedente titulada "Razonamiento" que explica el por qué. |
| **Las fuentes exportadas pueden conectarse a Tableau sin reprocesamiento manual** | ✓ | Los tres CSVs tienen tipos de datos limpios, surrogate keys enteras, y se conectan via Relationships en Tableau. Las instrucciones de conexión están en el doc de reglas, Sección 1. No se requiere ninguna transformación adicional. |

---

### D. Temas del curso cubiertos en esta entrega (según la matriz de cobertura, líneas 474-492)

La matriz de la propuesta indica que la Entrega 4 debe cubrir tres temas del curso:

| Tema del curso | ¿Se cubre? | Cómo se cubre |
|---|:---:|---|
| **Modelado analítico** | ✓ | Se extiende el Esquema en Estrella de la Entrega 3 con columnas adicionales, manteniendo la integridad relacional y las surrogate keys. Se documenta la estructura de Relationships para Tableau. |
| **Segmentación e insights** | ✓ | Segmentación ABC en 3 Tiers. Los insights derivados de la segmentación (ej. "29 países concentran el 79.5%") están documentados en el notebook y en el doc de reglas. |
| **Cálculos analíticos** | ✓ | Tres métricas derivadas (YoY, Share, MA3) + diseño de LODs y parámetros para Tableau. Cubre los cuatro sub-requisitos del tema 7 de la propuesta: métricas derivadas, porcentajes/participaciones, comparaciones relativas, y parámetros/filtros significativos. |

---

### E. Sub-requisitos obligatorios del tema 6 "Segmentación e interpretación" (líneas 165-171)

| Sub-requisito | ¿Se cumple? | Evidencia |
|---|:---:|---|
| Análisis por segmentos | ✓ | Los 252 países están clasificados en 3 Tiers. La tabla resumen del notebook muestra las estadísticas por Tier. |
| Comparación entre subgrupos | ✓ | Se comparan Tiers por número de países, volumen de exportaciones y porcentaje de participación. El doc de reglas explica cómo usar los Tiers para comparaciones en Tableau. |
| Mínimo 3 insights bien redactados | ✓ | Se cuentan como insights los hallazgos documentados: (1) 29 países concentran 79.5% del volumen, (2) los Top 5 del Share en 2021 son todos Tier 1, validando la segmentación, (3) el YoY positivo en 2021 para los top exportadores confirma el rebote post-COVID del Insight 3 de la Entrega 3. Estos insights se formalizarán más en la Entrega 5 con las visualizaciones, pero la evidencia numérica ya está aquí. |

---

### F. Sub-requisitos obligatorios del tema 7 "Cálculos analíticos" (líneas 173-180)

| Sub-requisito | ¿Se cumple? | Evidencia |
|---|:---:|---|
| Métricas derivadas | ✓ | YoY %, Share %, Promedio Móvil 3 años |
| Porcentajes o participaciones | ✓ | Share of Global Exports (%) |
| Acumulados o comparaciones relativas | ✓ | Cumulative_Share para la segmentación Pareto + comparación YoY relativa al año anterior |
| Parámetros o filtros significativos en Tableau | ✓ | Parámetro Top N (slider 5-50) y LODs diseñados |

---

## Resumen final

La Entrega 4 se construyó como una extensión natural de las entregas anteriores:

- La **segmentación** nació del Insight 1 de la Entrega 3 (distribución power-law).
- El **enriquecimiento del fact** fue necesario porque la Entrega 3 solo modeló Export, pero los análisis exploratorios usaban Import y Trade Balance.
- Las **métricas derivadas** se eligieron para responder a la pregunta analítica del proyecto.
- Los **parámetros** se diseñaron para dar interactividad con sentido en la Entrega 5.

Nada se hizo por cumplir un requisito en abstracto. Cada decisión tiene una cadena de razonamiento que conecta con hallazgos previos del propio proyecto.
