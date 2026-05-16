# Entrega 3 - Modelo de Datos, Métricas y Benchmarking Estructural

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Notebook asociado:** [`../notebooks/entrega3-pipeline-final.ipynb`](../notebooks/entrega3-pipeline-final.ipynb)

---

## 1. Justificación del Preprocesamiento para Llegar al Modelo

Es imperativo aclarar que **las tareas de limpieza de datos (manejo de nulos, atípicos, tipado de columnas, filtrado de entidades vigentes) ya fueron resueltas exhaustivamente durante el Entregable 2** y documentadas en su respectivo perfilado. Repetir esos pasos sería redundante e incorrecto.

Por lo tanto, el preprocesamiento exigido para esta entrega es **estrictamente de carácter estructural/arquitectónico**, ya que su propósito es transformar la matriz plana para que encaje en modelos relacionales analíticos. Los pasos ejecutados fueron:

1. **Validación de Unicidad y Cardinalidad:** Se aplicó una validación sobre la clave primaria compuesta (`Partner Name` + `Year`). *Justificación:* Evita que Tableau genere un producto cartesiano (explosión de datos) al cruzar tablas.
2. **Normalización (Resolución de Dependencias Transitivas):** Se aislaron las variables que no dependen directamente del flujo comercial. Por ejemplo, `Region` se separó de la transaccionalidad anual, y `World Growth (%)` se separó a la dimensión de tiempo. *Justificación:* Almacenar el crecimiento mundial en cada fila transaccional viola la 2da Forma Normal (2NF).
3. **Generación de Claves Subrogadas (Surrogate Keys):** Reemplazamos los identificadores alfanuméricos por identificadores numéricos incrementales o hashes (`dim_country_sk`). *Justificación:* Los *Joins* relacionales sobre enteros son computacionalmente mucho más rápidos.
4. **Construcción de la Tabla de Hechos:** Se eliminaron las descripciones textuales de la matriz principal, dejando solo identificadores y métricas aditivas (`Export USD`). 

---

## 2. Opciones de Arquitectura Comparadas

Para cumplir con el *brief* del proyecto, que exige evaluar al menos dos opciones de modelo además de la alternativa base, se diseñaron y evaluaron computacionalmente las siguientes **tres arquitecturas**:

*   **Alternativa Base: Tabla Plana (One Big Table - OBT)** 
    *   *Descripción:* El archivo directo e intacto exportado del Entregable 2, donde todo (países, regiones, aranceles, variables macroeconómicas) está desnormalizado en una sola sábana de datos.
*   **Opción 1: Esquema en Estrella (Star Schema)**
    *   *Descripción:* Desnormalización parcial. La información se separa lógicamente en una Tabla de Hechos central y dimensiones agrupadas (`Dim_Country` contiene tanto al país como a su región).
*   **Opción 2: Esquema Copo de Nieve (Snowflake Schema)**
    *   *Descripción:* Normalización completa (3NF). La dimensión país se disgrega aún más: `Dim_Country` se conecta a una nueva tabla `Dim_Region` mediante llaves foráneas.

---

## 3. Pruebas de Benchmarking y Criterios de Selección

Se programó un script computacional que somete las tres alternativas a evaluación. Estas métricas validan empíricamente la decisión final:

| Métrica Evaluada (Evidencia Empírica) | Alternativa Base (Tabla Plana) | Opción 1 (Esquema Estrella) | Opción 2 (Copo de Nieve) | Justificación de Decisión |
| :--- | :--- | :--- | :--- | :--- |
| **Sparsity / Memoria RAM (KB)** | Menor eficiencia (repite texto) | **Alta eficiencia** | Máxima compresión (3NF) | El Copo de Nieve ahorra marginalmente más memoria, pero ambas opciones relacionales aplastan a la Tabla Plana. |
| **Integridad Macro (Fan-Out Trap)** | Dato Distorsionado (Falso) | **Promedio Real** | **Promedio Real** | **CRÍTICO:** La Base duplica métricas agregadas globales por país. Las opciones 1 y 2 protegen la integridad matemática. |
| **Costo Topológico (Saltos de Join)** | Bajo (0 Joins) | **Moderado (1 Join directo)** | Alto (2 Joins en cascada) | El Copo de Nieve requiere unir Hechos -> País -> Región. En Tableau, los joins en cascada (Snowflaking) degradan la fluidez visual al filtrar. |

*(Nota: La tabla comparativa formal `tabla_comparativa_modelos.csv` ha sido generada automáticamente por el código y exportada).*

---

## 4. Definición del Modelo Seleccionado

**Modelo Seleccionado:** **Opción 1: Esquema en Estrella (Star Schema)**

**Justificación Final:** 
Dado el objetivo analítico del proyecto (cruzar variables Micro como "Exportaciones" con variables Macro como "Crecimiento Mundial"), la evidencia de la prueba del **Fan-Out Trap** obligó a descartar de inmediato la Alternativa Base (Tabla Plana). 

Entre las dos opciones restantes, se descartó la Opción 2 (Copo de Nieve) debido al **Costo Topológico**. Aunque ahorra algunos kilobytes extra de almacenamiento, obligaría a Tableau a realizar *Joins* en cadena para poder visualizar las métricas agrupadas por continente/región. 

El **Esquema en Estrella** ofrece el punto de equilibrio perfecto: protege la veracidad de las métricas económicas mundiales (sin forzar cálculos LOD) y permite que Tableau renderice visualizaciones a nivel Regional y de País con un solo salto (*Relationship*). Las tres tablas que componen la Estrella ganadora han sido exportadas a `/outputs/tableau_sources/`.
