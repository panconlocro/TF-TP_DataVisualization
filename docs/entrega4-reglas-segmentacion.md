# Entrega 4 — Reglas de Segmentación, Métricas Derivadas y Parámetros

## Proyecto

**Curso:** Data Visualization (1ACC0211) — UPC  
**Nombre del proyecto:** GlobalTradeAnalysis  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Notebook asociado:** [`../notebooks/entrega4-calculos-segmentacion.ipynb`](../notebooks/entrega4-calculos-segmentacion.ipynb)

| Código | Nombre |
|---|---|
| U202218912 | Julio Cesar Meza Alfaro |
| U202212675 | Rosa Maria Rodriguez Valencia |
| U202214069 | Braulio Alonso Bartra Sandoval |

---

## 1. Estructura Relacional para Tableau

### Esquema en Estrella (Star Schema — Kimball)

El modelo de datos seleccionado en la Entrega 3 es un **Esquema en Estrella** con surrogate keys enteras. En la Entrega 4 se enriqueció sin alterar la estructura relacional:

```
Fact_Trade ──► Dim_Country   (252 países — surrogate key int64: dim_country_sk)
           ──► Dim_Time      (34 años + World Growth % — surrogate key int64: dim_time_sk)
```

### Tablas exportadas (outputs/tableau_sources/)

| Tabla | Filas | Columnas | Descripción |
|:---|:---:|:---:|:---|
| `Fact_Trade.csv` | 7,783 | 9 | dim_time_sk, dim_country_sk, Export, Import, Trade Balance, Total Trade, Trade Status, AHS Weighted Avg, MFN Weighted Avg |
| `Dim_Country.csv` | 252 | 4 | dim_country_sk, Partner Name, Export_Tier, Total_Export_Hist |
| `Dim_Time.csv` | 34 | 3 | dim_time_sk, Year, World Growth (%) |
| `QA_Metricas_Derivadas.csv` | 7,783 | 8 | Tabla de referencia para QA (no para Tableau) |

### Conexión en Tableau

En Tableau se debe usar **Relationships** (no joins directos) para conectar las tres tablas:

1. Arrastrar `Fact_Trade` como tabla raíz.
2. Conectar `Dim_Country` mediante `dim_country_sk = dim_country_sk`.
3. Conectar `Dim_Time` mediante `dim_time_sk = dim_time_sk`.

**Por qué Relationships y no Joins:** Las Relationships de Tableau respetan la granularidad de cada tabla y no producen fan-out trap al agregar métricas de diferentes niveles de detalle. Si usáramos un join directo, `World Growth (%)` se repetiría por cada país del año, sesgando los promedios (exactamente el problema que la Entrega 3 identificó con la Tabla Plana).

### Por qué el Fact_Trade no contiene `World Growth (%)`

El crecimiento mundial es un atributo que depende **solo del año**, no del país. Si se incluyera en `Fact_Trade`, cada fila del año 2021 contendría el mismo valor, y un `AVG(World Growth)` produciría un promedio ponderado por el número de países activos en ese año — un resultado estadísticamente incorrecto. Al mantenerlo en `Dim_Time`, Tableau calcula el promedio sobre 34 valores (uno por año), que es el resultado correcto.

---

## 2. Reglas de Segmentación: Export Tier (ABC)

### Definición

Los 252 países se clasifican en tres segmentos basados en su **volumen total de exportaciones históricas** (suma 1988-2021), aplicando el principio de Pareto:

| Tier | Criterio | Países | % Países | % Export |
|---|---|:---:|:---:|:---:|
| **Tier 1 — Grandes Exportadores** | Acumulan hasta el 80% del volumen global | 29 | 11.5% | 79.5% |
| **Tier 2 — Exportadores Medianos** | Del 80% al 95% del volumen acumulado | 43 | 17.1% | 15.4% |
| **Tier 3 — Exportadores Pequeños** | Del 95% al 100% | 180 | 71.4% | 5.1% |

### Por qué se usa el volumen histórico total (no el último año)

- **Robustez:** El último año disponible (2021) es atípico por el rebote post-COVID (+21.8% YoY para EE.UU.). Clasificar solo por 2021 sobrerepresentaría a economías que se recuperaron más rápido.
- **Relevancia sostenida:** Un país que exportó mucho durante 20 años pero cayó en 2021 sigue siendo un actor relevante para el análisis longitudinal del proyecto.
- **Consistencia temporal:** La segmentación cubre el mismo período que el dataset (1988-2021), evitando sesgo por punto de corte.

### Cómo se usa en Tableau

La columna `Export_Tier` está en `Dim_Country`, por lo que en Tableau se puede:

- Filtrar por Tier (ej. ver solo Tier 1)
- Comparar Tiers lado a lado
- Usar como dimensión de color o forma
- Crear sets para análisis condicional

### Cómo afecta la interpretación

Sin la segmentación, los promedios globales están dominados por los ~30 países de Tier 1. Con la segmentación, se puede:

- Calcular medianas **dentro de cada Tier** para ver la distribución real.
- Detectar si un país de Tier 3 está creciendo a ritmos de Tier 2 (movilidad ascendente).
- Comparar la volatilidad (YoY) entre Tiers: ¿los grandes exportadores son más estables que los pequeños?

---

## 3. Métricas Derivadas

### 3.1 Variación Interanual (YoY %)

**Fórmula:**  
`Export_YoY_Pct = (Export_t - Export_{t-1}) / Export_{t-1} × 100`

**Cómo se calcula:**  
En Python: `groupby('Partner Name')['Export'].pct_change() * 100`  
En Tableau: Table Calculation `% Difference` particionada por `Partner Name`, ordenada por `Year`.

**Por qué importa para el proyecto:**  
La pregunta analítica del proyecto incluye entender la *dinámica* del comercio, no solo los niveles. Un país con $50B de exportaciones que creció 30% en un año es analíticamente más interesante que uno con $200B que creció 2%. El YoY captura esa dinámica.

**Cómo afecta la interpretación:**  
- Valores positivos → expansión comercial.
- Valores negativos → contracción.
- Valores extremos (>50% o <-50%) → shocks probables (crisis financiera, COVID, conflictos).
- El primer año de cada país es `NaN` (no hay año anterior para comparar).

### 3.2 Share of Global Exports (%)

**Fórmula:**  
`Export_Share_Pct = Export_país_año / SUM(Export_todos_países_año) × 100`

**Cómo se calcula:**  
En Python: División directa sobre `Global_Export_Year` (total por año).  
En Tableau (LOD):  
```
[Export (US$ Million)] / {FIXED [Year] : SUM([Export (US$ Million)])} * 100
```

**Por qué importa para el proyecto:**  
Las exportaciones absolutas crecen con la economía global. China pasó de $50B en 1988 a $2.4T en 2021, pero eso incluye el crecimiento global del comercio. El Share aísla la *participación relativa*, que es lo que realmente cambia la dinámica geopolítica comercial.

**Cómo afecta la interpretación:**  
- Un Share creciente → el país gana peso relativo en el comercio global.
- Un Share decreciente → el país pierde relevancia relativa, incluso si sus exportaciones crecen en términos absolutos.
- Debe sumar exactamente 100% por año (validado en el notebook: min=100.00%, max=100.00%).

### 3.3 Promedio Móvil 3 Años

**Fórmula:**  
`Export_MA3 = mean(Export_{t-2}, Export_{t-1}, Export_t)`

**Cómo se calcula:**  
En Python: `rolling(3, min_periods=1).mean()` por país.  
En Tableau: `WINDOW_AVG(SUM([Export]), -2, 0)` particionada por país.

**Por qué importa para el proyecto:**  
Las exportaciones anuales tienen volatilidad por factores coyunturales (precios de commodities, tipos de cambio, shocks). El promedio móvil suaviza esa volatilidad y revela la tendencia de mediano plazo, que es más útil para la toma de decisiones que el valor puntual.

**Cómo afecta la interpretación:**  
- Si la línea real está consistentemente por encima del MA3 → aceleración.
- Si está por debajo → desaceleración.
- La divergencia entre el valor real y el MA3 señala puntos de inflexión.

---

## 4. Parámetros y Lógica Analítica para Tableau

### 4.1 Parámetro: Top N Países

**Definición en Tableau:**  
- Tipo: Integer  
- Rango: 5 a 50  
- Valor por defecto: 10  
- Nombre del parámetro: `p_Top_N`

**Uso:**  
Se crea un campo calculado que marca si un país está en el Top N de exportaciones del año seleccionado:

```
// Campo calculado: Is_Top_N
RANK(SUM([Export (US$ Million)])) <= [p_Top_N]
```

Luego se usa como filtro en las vistas de ranking (equivalente a la visualización V01 de la Entrega 3, pero interactiva).

**Por qué un parámetro y no un filtro fijo:**  
Un filtro fijo obliga al diseñador a elegir un N arbitrario. El parámetro delega esa decisión al usuario del dashboard, que puede ajustar el nivel de detalle según su necesidad. Un analista de políticas públicas puede querer ver Top 50; un ejecutivo puede preferir Top 5.

### 4.2 Cálculo LOD: Total Global por Año (para Share)

**Definición en Tableau:**

```
// Campo calculado: Global_Export_Year
{FIXED [Year] : SUM([Export (US$ Million)])}
```

```
// Campo calculado: Export_Share_Pct
SUM([Export (US$ Million)]) / [Global_Export_Year] * 100
```

**Por qué un LOD y no una Table Calculation:**  
- El LOD `{FIXED [Year]}` es **independiente de los filtros de la vista**. Si el usuario filtra por un Tier o una región, el denominador del Share sigue siendo el total global del año, no el total filtrado.
- Una Table Calculation `% of Total` se recalcularía sobre las filas visibles, produciendo un Share distorsionado.

### 4.3 Cálculo LOD: Exportación Promedio por Tier y Año

**Definición en Tableau:**

```
// Campo calculado: Avg_Export_By_Tier_Year
{FIXED [Export_Tier], [Year] : AVG([Export (US$ Million)])}
```

**Para qué sirve:**  
Permite crear una línea de referencia por Tier en gráficos temporales. Así, un usuario puede ver la exportación de un país específico versus el promedio de su Tier, evaluando si está por encima o por debajo de sus pares.

---

## 5. Resumen de cambios respecto a la Entrega 3

| Componente | Entrega 3 | Entrega 4 |
|---|---|---|
| `Fact_Trade` columnas | 3 (dim_time_sk, dim_country_sk, Export) | 9 (+Import, Trade Balance, Total Trade, Trade Status, AHS Weighted Avg, MFN Weighted Avg) |
| `Dim_Country` columnas | 2 (dim_country_sk, Partner Name) | 4 (+Export_Tier, Total_Export_Hist) |
| `Dim_Time` | Sin cambios | Sin cambios |
| Segmentación | No existía | Export_Tier (ABC, 3 niveles) |
| Métricas derivadas | No existían | YoY %, Share %, MA3 (QA en Python; diseño para Tableau) |
| Parámetros Tableau | No diseñados | Top N, LOD Share, LOD Avg por Tier |
