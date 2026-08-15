# Entrega 3 - Modelo de Datos, Métricas y Benchmarking Estructural

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Nombre del proyecto:** GlobalTradeAnalysis  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Notebook asociado:** [`../notebooks/entrega3-pipeline-final.ipynb`](../notebooks/entrega3-pipeline-final.ipynb)

---

## 1. Justificación del Preprocesamiento para Llegar al Modelo

Es imperativo aclarar que **las tareas de limpieza de datos (manejo de nulos, atípicos, tipado de columnas, filtrado de entidades vigentes) ya fueron resueltas exhaustivamente durante el Entregable 2** y documentadas en `docs/entregable2_documentacion_detallada.md`. Repetir esos pasos sería redundante e incorrecto.

Por lo tanto, el preprocesamiento exigido para esta entrega es **estrictamente de carácter estructural/arquitectónico**, ya que su propósito es transformar la matriz plana para que encaje en modelos relacionales analíticos. Los pasos ejecutados son comunes a las dos opciones evaluadas:

1. **Validación de Unicidad (Paso 1):** Se verificó que `(Partner Name, Year)` sea clave primaria única en el dataset. *Justificación:* Sin esta garantía, cualquier join produce un producto cartesiano que infla artificialmente las métricas y vuelve inútil la comparación entre modelos.

2. **Normalización 2NF — Extracción de `World Growth (%)` (Paso 2):** Esta variable depende funcionalmente solo del año, no del país. Almacenarla en cada fila transaccional viola la Segunda Forma Normal (2NF) y produce **fan-out trap** al agregar sobre ella. Se extrae a `Dim_Macro_3NF` en el modelo 3NF y a `Dim_Time` en el Esquema en Estrella.

3. **Tipo de clave (diferencia central entre los dos modelos, Paso 3):** Ambos modelos normalizan las mismas dependencias funcionales, pero difieren en el tipo de clave foránea usada en la tabla de hechos. El **Modelo 3NF (Inmon)** mantiene `Partner Name` (string) como FK en el fact; el **Esquema en Estrella (Kimball)** lo reemplaza por `dim_country_sk` (int64). Esta elección es la fuente principal de divergencia en las métricas 1 y 4 del benchmarking.

4. **Tabla de Hechos angosta (Paso 4):** En ambos modelos el fact queda reducido a 3 columnas (2 FKs + 1 métrica aditiva), eliminando toda redundancia descriptiva de la tabla principal.

---

## 2. Opciones de Arquitectura Comparadas

Para cumplir con el *brief* del proyecto, que exige evaluar al menos dos opciones además de la alternativa base, se diseñaron y evaluaron computacionalmente las siguientes **tres arquitecturas**:

- **Alternativa Base — Tabla Plana (One Big Table, OBT)**  
  El archivo directo e intacto exportado del Entregable 2. Todo (países, dimensión temporal, aranceles, variables macroeconómicas) está desnormalizado en una sola matriz sin separación lógica de entidades.

- **Opción 1 — Modelo Relacional 3NF (Inmon) con claves naturales**  
  Normalización en Tercera Forma Normal. Las tablas se derivan de las dependencias funcionales del dataset sin introducir surrogate keys artificiales:
  - `Dim_Partners_3NF(partner_name)` — clave natural string
  - `Dim_Macro_3NF(year, world_growth)` — clave natural integer
  - `Fact_Trade_3NF(partner_name FK, year FK, export)` — FK textual sobre `partner_name`

- **Opción 2 — Esquema en Estrella (Kimball) con surrogate keys enteras**  
  Modelo dimensional que resuelve las mismas dependencias funcionales que 3NF pero reemplaza las claves naturales por enteros incrementales:
  - `Dim_Country(dim_country_sk, partner_name)` — surrogate key int64
  - `Dim_Time(dim_time_sk, year, world_growth)` — surrogate key int64
  - `Fact_Trade(dim_time_sk FK, dim_country_sk FK, export)` — FK exclusivamente int64

---

## 3. Pruebas de Benchmarking y Criterios de Selección

Se programó un script computacional que somete las tres alternativas a cuatro métricas empíricas. Los valores son reproducibles ejecutando la celda 7 del notebook asociado.

| Métrica Analítica | Tabla Plana (Base) | 3NF Inmon (Opción 1) | Estrella (Opción 2) | Conclusión |
| :--- | :--- | :--- | :--- | :--- |
| **Memoria RAM (KB)** | ~3 432 KB | ~660 KB | **~200 KB** | La Tabla Plana repite columnas descriptivas en cada fila transaccional. El 3NF normaliza dimensiones pero mantiene `Partner Name` como FK string (7 783 strings repetidos en el fact). La Estrella reemplaza ese string por int64 → mínima huella en la tabla de hechos. |
| **Integridad Macro — Fan-Out Trap (`Avg World Growth %`)** | **Distorsionado (falso)** | ✓ real | ✓ real | La Tabla Plana repite `World Growth (%)` una vez por país/año: su promedio queda ponderado por el N de países activos en cada año → fan-out trap. 3NF y Estrella aíslan el indicador en tablas anuales dedicadas: un único valor por año garantiza el promedio verdadero. **Este criterio descarta la Tabla Plana.** |
| **Anomalía de Actualización (filas afectadas si se corrige un año)** | N filas (una por país activo en 2010) | **1 fila** (en `Dim_Macro_3NF`) | **1 fila** (en `Dim_Time`) | Al aislar `World Growth` en tablas propias, 3NF y Estrella logran que una corrección del Banco Mundial sobre el dato de un año requiera actualizar exactamente 1 fila. En la Tabla Plana la corrección se propaga a todas las filas del año. 3NF y Estrella empatan en esta métrica. |
| **Anomalía de Nombre (filas afectadas si un país cambia nombre oficial)** | N filas (en dataset completo) | **N+1 filas** (fact + dim; FK es string) | **1 fila** (`Dim_Country`; fact intacto) | En la Tabla Plana y en 3NF el `Partner Name` es texto en el fact: un cambio de nombre exige actualizar cada fila que lo referencie. Paradójicamente, 3NF es marginalmente peor que la Tabla Plana: requiere las mismas N filas del fact más 1 fila adicional en `Dim_Partners_3NF`. La Estrella es inmune: el fact solo almacena el surrogate int64; basta modificar 1 fila en `Dim_Country`. **Este criterio descarta 3NF.** |

*(La tabla `tabla_comparativa_modelos.csv` ha sido generada automáticamente por el código y exportada a `/outputs/`.)*

---

## 4. Definición del Modelo Seleccionado

**Modelo Seleccionado: Opción 2 — Esquema en Estrella (Star Schema — Kimball)**

La decisión se basa exclusivamente en la evidencia empírica del benchmarking de la sección anterior.

| Criterio | Tabla Plana (Base) | 3NF Inmon (Opción 1) | Estrella (Opción 2) | Veredicto |
| :--- | :---: | :---: | :---: | :--- |
| Memoria RAM | ~3 432 KB | ~660 KB | **~200 KB** | Estrella minimiza la huella |
| Integridad `World Growth (%)` | distorsionado | ✓ real | ✓ real | **Descarta Tabla Plana** |
| Anomalía de actualización | N filas/año | 1 fila en Dim_Macro | 1 fila en Dim_Time | 3NF y Estrella empatan |
| Anomalía de nombre | N filas | **N+1 filas** | **1 fila** en Dim_Country | **Descarta 3NF** |

**Razonamiento de la decisión en dos pasos:**

**Paso 1 — Descarte de la Tabla Plana (fan-out trap).**  
La métrica de integridad macro revela que la Tabla Plana produce un promedio de `World Growth (%)` estadísticamente incorrecto porque el valor se repite por cada país activo en el año, sesgando la agregación según el N de países con datos. Dado que el objetivo analítico del proyecto incluye cruzar variables micro (exportaciones por país) con variables macro (crecimiento mundial), operar sobre una Tabla Plana introduciría error sistemático en cualquier cálculo de promedios o tendencias globales. La Tabla Plana queda descartada en este punto.

**Paso 2 — Descarte del Modelo 3NF (anomalía de nombre por FK string).**  
El Modelo 3NF (Inmon) mejora significativamente sobre la Tabla Plana: resuelve el fan-out trap (métrica 2) y la anomalía de actualización de `World Growth` (métrica 3). Sin embargo, presenta una debilidad estructural crítica: al conservar `Partner Name` (string) como clave foránea en la tabla de hechos, cualquier cambio en el nombre oficial de un país exige actualizar **cada fila del fact** que referencie ese país. Paradójicamente, el costo es mayor que en la Tabla Plana, ya que requiere las mismas N filas del fact más 1 fila adicional en `Dim_Partners_3NF`. En un dataset con 252 países y 34 años de historia, esto representa un riesgo de integridad referencial no trivial. El Modelo 3NF queda descartado.

**El Esquema en Estrella** resuelve ambos problemas: elimina el fan-out trap al aislar `World Growth` en `Dim_Time`, y es estructuralmente inmune a las anomalías de nombre mediante surrogate keys enteras. Adicionalmente, los joins sobre `int64` son más eficientes computacionalmente que sobre `varchar`, ventaja relevante en Tableau con datasets de decenas de miles de filas. La estructura final exportada es:

```
Fact_Trade ──► Dim_Country   (252 países — surrogate key int64: dim_country_sk)
           ──► Dim_Time      (34 años + World Growth % — surrogate key int64: dim_time_sk)
```

Las tres tablas del modelo ganador han sido exportadas a `/outputs/tableau_sources/` listas para conectar en Tableau:

| Tabla | Filas | Columnas | Descripción |
|:---|:---:|:---:|:---|
| `Fact_Trade.csv` | 7 783 | 3 | dim_time_sk, dim_country_sk, Export (US$ Million) |
| `Dim_Country.csv` | 252 | 2 | dim_country_sk, Partner Name |
| `Dim_Time.csv` | 34 | 3 | dim_time_sk, Year, World Growth (%) |
