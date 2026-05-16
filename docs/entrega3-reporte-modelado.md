# Entrega 3 - Modelo de Datos, Métricas y Benchmarking Estructural

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Notebook asociado:** [`../notebooks/entrega3-pipeline-final.ipynb`](../notebooks/entrega3-pipeline-final.ipynb)

---

## 1. Justificación del Preprocesamiento Estructural (Hacia el Modelo)

Es imperativo aclarar que **las tareas de limpieza de calidad de datos (manejo de nulos, imputación, filtrado de entidades) ya fueron resueltas y documentadas exhaustivamente durante el Entregable 2**. 

El preprocesamiento para esta entrega es **estrictamente arquitectónico**, cuyo propósito es transformar esa matriz plana y limpia en un modelo relacional analítico óptimo. Los pasos y sus justificaciones fueron:

1. **Validación de Unicidad (País-Año):** Si la tabla original presenta duplicados en sus llaves, la conexión en Tableau generaría un "producto cartesiano", multiplicando falsamente los montos transaccionales.
2. **Normalización Dimensional:** Variables descriptivas (`Region`) y macroeconómicas (`World Growth (%)`) se separaron. Almacenar el crecimiento mundial en cada fila de exportación viola la 2da Forma Normal y genera redundancia perjudicial para Tableau.
3. **Generación de Claves Subrogadas (Surrogate Keys):** Los nombres de los países (`Partner Name`) fueron sustituidos por identificadores numéricos. Justificación: Los *Joins* sobre valores enteros (`Int`) reducen masivamente la carga de CPU frente a cruzamientos con cadenas de texto (`String`).
4. **Construcción de la Tabla de Hechos:** Generación de la tabla central depurada de textos descriptivos, albergando únicamente métricas numéricas.

---

## 2. Opciones de Arquitectura Comparadas

Se evaluaron dos enfoques para inyectar la información a Tableau:

*   **Opción A (Modelo Base): Tabla Plana (One Big Table - OBT)** 
    *   *Descripción:* Conectar el archivo `dataset_limpio_entrega2_consolidado.csv` intacto. Todo desnormalizado.
*   **Opción B (Modelo Seleccionado): Esquema en Estrella (Star Schema)**
    *   *Descripción:* El output procesado en este entregable. Separación analítica de la información mediante *Relationships* nativas.

---

## 3. Matriz Extendida de Benchmarking y Criterios Arquitectónicos

Para sustentar la elección de la Opción B, no recurrimos a preferencias estéticas. Programamos un script de evaluación (`notebooks/entrega3-pipeline-final.ipynb`) que arroja evidencias empíricas (Rendimiento) y arquitectónicas (Business Intelligence):

| Criterio Evaluado | Resultado OBT (Tabla Plana) | Resultado Estrella (Modelo Final) | Justificación para el Objetivo del Proyecto |
| :--- | :--- | :--- | :--- |
| **1. Compresión de Memoria (RAM / Disco)** | Menor eficiencia | **Mayor compresión** | Eficiencia indispensable para procesar visualmente más de 30 años de comercio mundial sin retraso de *rendering*. |
| **2. Fidelidad Semántica (Fan-Out Trap)** | Agregación Destruida / Falsa | **Promedio Real Conservado** | **CRÍTICO:** Evita la distorsión matemática de promedios al cruzar volúmenes micro con tasas macro (Ej: World Growth). |
| **3. Complejidad Analítica (Uso de LODs)** | Alta (Requiere *{FIXED}* LODs) | **Nula (Cálculos directos)** | Acelera la construcción del *Dashboard* liberando al usuario de programar complejas expresiones de corrección. |
| **4. Riesgo de Update Anomaly** | Crítico (Alterar N filas) | **Inexistente** | Facilita la corrección de datos. Si una nación cambió de denominación entre 1989 y 2023, basta alterar un único registro. |
| **5. Escalabilidad (Conformed Dimensions)** | Rígida / Ineficiente | **Flexible** | Permite incorporar nuevas capas (ej. PIB del Banco Mundial) en entregas futuras de manera limpia a nivel país o año. |

*(Nota: La evidencia tabular formal `tabla_comparativa_modelos.csv` ha sido automatizada y reside en `/outputs/`).*

---

## 4. Conclusión y Artefactos

Dado el objetivo transversal de analizar dinámicas económicas cruzadas, el **Esquema en Estrella** resuelve contundentemente la incapacidad de la Tabla Plana para sostener variables macroeconómicas sin incurrir en trampas de agregación (Fan-Out). 

Los tres componentes estructurales definitivos (`Fact_Trade.csv`, `Dim_Country.csv`, `Dim_Time.csv`) se encuentran en `/outputs/tableau_sources/`, respaldados por una arquitectura probada, medible y escalable.
