# Entrega 3 - Modelo de Datos, Métricas y Benchmarking Estructural

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Notebook asociado:** [`../notebooks/entrega3-preprocesamiento-modelado.ipynb`](../notebooks/entrega3-preprocesamiento-modelado.ipynb)

---

## 1. Preprocesamiento Real sobre el Dataset

Para asegurar que Tableau procese los datos con máximo rendimiento y sin errores de agregación, aplicamos un preprocesamiento orientado al **Modelado Dimensional (Metodología de Ralph Kimball)** sobre el *dataset* limpio de la Entrega 2. Los pasos fueron:

1. **Filtrado de Entidades y Control de Calidad:** Se descartaron registros con `entity_status == 'Inactivo'` y se limpiaron valores nulos en las métricas core (`Export USD`).
2. **Generación de Variables Derivadas:** Se creó la variable `Decade` (Década) agrupando la columna temporal para permitir segmentación transversal a largo plazo en Tableau.
3. **Generación de Surrogate Keys (Claves Subrogadas):** En lugar de realizar uniones (Joins) usando el nombre del país (`Partner Name`) en formato `String`, se generaron claves enteras (`dim_country_sk`, `dim_time_sk`). Las comparaciones de enteros en memoria son órdenes de magnitud más rápidas.
4. **Desagregación:** Se dividió la matriz unificada en dimensiones (geográfica y temporal) y una tabla central transaccional (Hechos).

---

## 2. Discusión de Opciones de Modelo de Datos

Se plantearon tres arquitecturas analíticas para ser consumidas por Tableau. Cada una representa un *trade-off* entre rendimiento de consulta, integridad de datos y facilidad de uso.

### Opción A: Tabla Plana (One Big Table - OBT)
*   **Definición:** Todas las jerarquías, dimensiones y hechos se desnormalizan en una sola matriz gigantesca (similar al output de la Entrega 2).
*   **Debilidad Crítica:** Falla en la integridad semántica. Genera un riesgo altísimo de **Fan-out trap** al duplicar métricas agregadas globales por cada país existente en un año determinado.

### Opción B: Esquema Copo de Nieve (Snowflake Schema)
*   **Definición:** Modelo altamente normalizado (Tercera Forma Normal - 3NF). 
*   **Debilidad Crítica:** La sobre-normalización obliga a Tableau a resolver múltiples "saltos" (Joins en cadena) en tiempo de ejecución, lo que degrada la interactividad del Dashboard, violando el principio de fluidez visual.

### Opción C: Esquema en Estrella (Star Schema)
*   **Definición:** Una tabla de Hechos central transaccional rodeada de dimensiones desnormalizadas.
*   **Fortaleza:** Es el estándar de la industria (Kimball). Las dimensiones "conformadas" permiten cortes analíticos limpios y ahorra los joins complejos en Tableau al conectarse mediante su capa lógica (*Relationships*).

---

## 3. Pruebas de Estrés y Evidencia Computacional (Benchmarking)

Para cumplir estrictamente con el criterio de *"selección de modelo justificado con evidencia"*, el código en Python ejecuta métricas de evaluación estructurales midiendo los beneficios en KB y la precisión estadística:

| Métrica Computacional (Evidencia Empírica) | Resultado en OBT (Tabla Plana) | Resultado en Estrella (Star Schema) | Conclusión Basada en Evidencia |
| :--- | :--- | :--- | :--- |
| **Consumo de Memoria RAM (Sparsity)** | Muy ineficiente (repite *strings*) | Eficiente (Surrogate Keys) | **La Estrella ahorra RAM drásticamente.** Eliminar la redundancia textual disminuye el peso, lo que asegura que Tableau cargue el Extracto más rápido. |
| **Prueba de Fan-Out Trap (Fidelidad Semántica)** | Distorsiona el `World Growth (%)` | Mantiene el Promedio Real | **La OBT corrompe la agregación nativa.** Este es el hallazgo más crítico: si usamos la OBT original, el Dashboard arrojará promedios macroeconómicos falsos. |

---

## 4. Definición del Modelo Seleccionado

**Modelo Seleccionado:** **Esquema en Estrella (Star Schema) implementado en la Capa Lógica (Relationships) de Tableau.**

**Justificación basada en evidencia:**
Como se demuestra matemáticamente en las pruebas del notebook, el Esquema en Estrella no es solo una "buena práctica teórica", sino una necesidad computacional y aritmética para el proyecto.

Se rechaza definitivamente la Tabla Plana porque la prueba del **Fan-Out Trap** demuestra empíricamente que corrompe la precisión de las métricas macroeconómicas al duplicarlas. Para la "Dinámica del comercio mundial", donde compararemos constantemente tasas globales de crecimiento con sumatorias de volumen local, la integridad matemática que provee la Estrella (junto con su probada compresión de memoria) es la única arquitectura viable para desplegar un Dashboard profesional.
