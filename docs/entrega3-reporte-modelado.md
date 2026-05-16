# Entrega 3 - Modelo de Datos, Métricas y Benchmarking Estructural

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Notebook asociado:** [`../notebooks/entrega3-pipeline-final.ipynb`](../notebooks/entrega3-pipeline-final.ipynb)

---

## 1. Justificación del Preprocesamiento para Llegar al Modelo

Es imperativo aclarar que **las tareas de limpieza de datos (manejo de nulos, atípicos, tipado de columnas, filtrado de entidades vigentes) ya fueron resueltas exhaustivamente durante el Entregable 2** y documentadas en su respectivo perfilado. Repetir esos pasos sería redundante e incorrecto.

Por lo tanto, el preprocesamiento exigido para esta entrega es **estrictamente de carácter estructural/arquitectónico**, ya que su propósito es transformar la matriz original (generada en la Entrega 2) para que encaje en el modelo relacional analítico. Los pasos ejecutados y justificados fueron:

1. **Validación de Unicidad y Cardinalidad:** Se aplicó una validación sobre la clave primaria compuesta (`Partner Name` + `Year`). *Justificación:* Si existen duplicados en este nivel base, al conectar las tablas en Tableau el motor Hyper generaría un producto cartesiano (explosión de datos), arruinando los cálculos agregados.
2. **Normalización (Resolución de Dependencias Transitivas):** Se aislaron las variables que no dependen directamente del flujo comercial. Por ejemplo, `Region` se separó a la dimensión de país, y `World Growth (%)` a la dimensión de tiempo. *Justificación:* Almacenar el crecimiento mundial en cada fila transaccional viola la 2da Forma Normal (2NF) y genera redundancia analítica masiva.
3. **Generación de Claves Subrogadas (Surrogate Keys):** Reemplazamos los identificadores alfanuméricos (`Partner Name`) por identificadores numéricos incrementales o hashes (`dim_country_sk`). *Justificación:* Los *Joins* relacionales sobre enteros son computacionalmente mucho más rápidos para el servidor de Tableau que las evaluaciones cruzadas de cadenas de texto.
4. **Construcción de la Tabla de Hechos:** Se eliminaron las descripciones textuales de la matriz principal, dejando solo identificadores y métricas aditivas (`Export USD`). *Justificación:* Centraliza el almacenamiento transaccional para operaciones aritméticas eficientes.

---

## 2. Opciones de Arquitectura Comparadas

Se evaluaron dos modelos de datos competitivos para inyectar la información a Tableau:

*   **Opción A (Modelo Base): Tabla Plana (One Big Table - OBT)** 
    *   *Descripción:* El archivo directo e intacto exportado del Entregable 2 (`dataset_limpio_entrega2_consolidado.csv`), donde todo está desnormalizado.
*   **Opción B (Modelo Avanzado): Esquema en Estrella (Star Schema)**
    *   *Descripción:* El output del preprocesamiento de este entregable. La información se separa lógicamente en Hechos y Dimensiones, que se vincularán usando *Relationships* nativas de Tableau.

---

## 3. Pruebas de Benchmarking y Criterios de Selección

Se programó un script computacional que somete ambos modelos a evaluación utilizando métricas empíricas. Estas pruebas validan por qué la **Opción B (Esquema en Estrella)** es requerida:

| Métrica Evaluada (Evidencia) | Resultado OBT (Tabla Plana) | Resultado Estrella (Star Schema) | Justificación de Decisión para el Modelo |
| :--- | :--- | :--- | :--- |
| **Consumo de Memoria RAM (Sparsity)** | Menor eficiencia | **Mayor compresión** | El modelo Estrella ahorra memoria al descartar los textos duplicados; esto es necesario para garantizar fluidez operativa en Tableau al filtrar décadas enteras. |
| **Riesgo de Agregación (Fan-Out Trap)** | Dato Distorsionado / Falso | **Promedio Real Conservado** | **CRÍTICO:** La OBT suma o promedia múltiples veces el crecimiento macroeconómico global por cada país que existe. La Estrella resuelve el problema del Fan-Out, evitando métricas falsas sin forzar al usuario a programar complejos Level-of-Detail (LODs) en Tableau. |

*(Nota: La tabla comparativa formal `tabla_comparativa_modelos.csv` ha sido generada automáticamente por el código y se encuentra en `/outputs/`).*

---

## 4. Definición del Modelo Seleccionado

**Modelo Seleccionado:** **Esquema en Estrella (Star Schema)**

**Justificación Final:** 
Dado el objetivo analítico del proyecto (cruzar variables transaccionales Micro como Exportaciones Nacionales con variables contextuales Macro como Crecimiento Mundial), la evidencia de la prueba del **Fan-Out Trap** descartó irrevocablemente el Modelo Base (Tabla Plana). Mantener la OBT hubiese significado inyectar datos propensos a fallos estadísticos si el analista final no estaba vigilante. 

El preprocesamiento estructural que ejecutamos garantizó que el modelo seleccionado asegure velocidad de cómputo (vía *Surrogate Keys*) y precisión semántica natural. Las tres tablas que lo componen han sido serializadas y están listas para su consumo en `/outputs/tableau_sources/`.
