# Entrega 3 - Modelo de Datos, Métricas y Benchmarking Estructural

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Tema:** Dinámica del comercio mundial: exportaciones e importaciones por país, categoría de producto y región geográfica (1989-2023)  
**Notebook asociado:** [`../notebooks/entrega3-benchmarking-modelado.ipynb`](../notebooks/entrega3-benchmarking-modelado.ipynb)

---

## 1. Preprocesamiento Avanzado para el Modelo Dimensional

Para asegurar que Tableau procese los datos con máximo rendimiento y sin errores de agregación, se aplicó un preprocesamiento orientado al **Modelado Dimensional (Metodología de Ralph Kimball)**. Los pasos, justificados técnicamente, son:

1. **Resolución de Granularidad y Dependencias Funcionales:** Se verificó que el nivel de detalle (LOD) base del dataset es `Country-Year`. Se detectó que atributos como el crecimiento mundial (`World Growth`) dependían solo del año, mientras que los aranceles (`AHS`) dependían del cruce. Se separaron las variables para cumplir con la Segunda Forma Normal (2NF).
2. **Generación de Surrogate Keys (Claves Subrogadas):** En lugar de realizar uniones (Joins) usando el nombre del país (`Partner Name`) en formato `String`, se generaron claves enteras (`dim_country_sk`, `dim_time_sk`). Las comparaciones de enteros en memoria son órdenes de magnitud más rápidas que las comparaciones de texto.

---

## 2. Discusión de Opciones de Modelo de Datos

Se plantearon tres arquitecturas analíticas para ser consumidas por Tableau. Cada una representa un *trade-off* entre rendimiento de consulta, integridad de datos y facilidad de uso.

### Opción A: Tabla Plana (One Big Table - OBT)
*   **Definición:** Todas las jerarquías, dimensiones y hechos se desnormalizan en una sola matriz gigantesca.
*   **Debilidad Crítica:** Falla en la integridad semántica. Genera un riesgo altísimo de **Fan-out trap** al duplicar métricas agregadas por cada país existente.

### Opción B: Esquema Copo de Nieve (Snowflake Schema)
*   **Definición:** Modelo altamente normalizado (Tercera Forma Normal - 3NF). 
*   **Debilidad Crítica:** La sobre-normalización obliga a Tableau a resolver múltiples "saltos" (Joins en cadena) en tiempo de ejecución, lo que degrada la interactividad del Dashboard, violando el principio de fluidez visual.

### Opción C: Esquema en Estrella (Star Schema)
*   **Definición:** Una tabla de Hechos central transaccional rodeada de dimensiones desnormalizadas.
*   **Fortaleza:** Es el estándar de la industria (Kimball). Las dimensiones "conformadas" permiten cortes analíticos limpios y ahorra los joins complejos en Tableau al conectarse mediante su capa lógica (*Relationships*).

---

## 3. Pruebas de Estrés y Evidencia Computacional (Benchmarking)

Para cumplir estrictamente con el criterio de *"selección de modelo justificado con evidencia y no solo preferencias técnicas"*, programamos un script de pruebas de estrés (Benchmarking) en Python simulando **1 Millón de transacciones**. Las pruebas arrojaron la siguiente **evidencia dura**:

| Prueba / Métrica Empírica | Resultado en OBT (Tabla Plana) | Resultado en Estrella (Star Schema) | Conclusión Basada en Evidencia |
| :--- | :--- | :--- | :--- |
| **Evidencia A: Consumo de RAM (Sparsity)** | ~114 MB en memoria | ~22 MB en memoria | **La Estrella es 5x más eficiente.** Elimina la redundancia de strings, lo que asegura que Tableau cargue el Extracto de forma casi instantánea. |
| **Evidencia B: Latencia de Exportación (I/O)** | 2.5 a 3.0 segundos | 0.4 a 0.6 segundos | **La Estrella reduce el tiempo de I/O en un 80%.** Los tiempos de recarga programados en Tableau Server serán marginales. |
| **Evidencia C: Prueba de Fan-Out Trap** | Promedio de Crecimiento: 3.89% (Falso) | Promedio de Crecimiento: 3.01% (Real) | **La OBT corrompe la agregación nativa.** Este es el hallazgo más crítico: si usamos OBT, el Dashboard arrojará datos falsos a menos que se sobrecargue de cálculos LoD. |
| **Evidencia D: Latencia de Actualización** | ~0.0150 segundos (Afecta N filas) | ~0.0009 segundos (Afecta 1 fila) | **La Estrella es 15x más rápida al mutar datos.** Si hay correcciones históricas, el impacto computacional es nulo. |

---

## 4. Definición del Modelo Seleccionado

**Modelo Seleccionado:** **Esquema en Estrella (Star Schema) implementado en la Capa Lógica (Relationships) de Tableau.**

**Justificación basada en evidencia:**
Como demuestran matemáticamente las 4 pruebas de estrés (Evidencias A, B, C y D), el Esquema en Estrella no es solo una "buena práctica teórica", sino una necesidad computacional y aritmética para este proyecto.

Se rechaza definitivamente la Tabla Plana porque la prueba **Evidencia C** demuestra que corrompe la precisión de las métricas macroeconómicas (el Fan-Out Trap distorsiona la media real). Para la "Dinámica del comercio mundial", donde comparamos constantemente tasas globales con sumatorias locales, la integridad matemática que provee la Estrella (junto con su reducción de peso en disco demostrada en la **Evidencia A**) es la única arquitectura viable para desplegar un Dashboard profesional sin retrasos de renderizado.
