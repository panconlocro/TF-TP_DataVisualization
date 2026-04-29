# Propuesta de Trabajo Final con Entregas Parciales

Curso: `Data Visualization`

Enfoque recomendado del curso:

- Herramienta principal: `Tableau`
- Soporte técnico y analítico: `Python` con notebooks
- Enfoque metodológico: perfilado, limpieza, modelado, análisis exploratorio, diseño visual, storytelling, accesibilidad, dashboards e integración de una técnica avanzada

## Nombre sugerido del trabajo final

**Proyecto Integrador de Visualización de Datos para la Toma de Decisiones**

## Idea central del trabajo final

El trabajo final debe consistir en el desarrollo de un producto integral de visualización de datos que permita responder una pregunta real de negocio, gestión, política pública, investigación o monitoreo operativo.

El proyecto debe cubrir el ciclo completo visto en clase:

1. Comprensión del problema
2. Selección y evaluación de la fuente de datos
3. Perfilado del dato
4. Limpieza y preparación
5. Modelado o estructuración analítica
6. Análisis exploratorio
7. Selección de gráficos
8. Construcción de insights
9. Storytelling con datos
10. Accesibilidad y diseño visual
11. Análisis longitudinal
12. Análisis transversal o comparativo
13. Construcción de dashboard final
14. Componente técnico avanzado
15. Defensa metodológica y visual

## Objetivo general

Diseñar, construir y defender un dashboard o producto visual interactivo en `Tableau`, sustentado en un pipeline reproducible en `Python`, que permita responder una pregunta analítica relevante con claridad, rigor técnico y valor para la toma de decisiones.

## Modalidad sugerida

- Trabajo en equipos de `2` a `3` estudiantes.
- Si el curso requiere, también puede adaptarse a modalidad individual.
- El equipo debe mantener una línea temática coherente durante todo el ciclo.

## Producto final esperado

Cada equipo debe entregar:

- Un `dashboard final` en `Tableau`.
- Una `historia visual` o secuencia narrativa breve.
- Un `set de notebooks` o notebook integrador en `Python`.
- Una `base de datos final` o archivos `CSV` preparados para Tableau.
- Una `bitácora técnica` de limpieza, transformación y validación.
- Una `presentación final` con defensa técnica y analítica.

## Configuración mínima del producto final

Para asegurar que el trabajo final integre realmente todo lo visto en clase, el producto final debe contener como mínimo:

- `1` problema analítico claramente formulado y acotado.
- `1` usuario objetivo principal y `1` escenario concreto de uso.
- `1` dataset principal validado y, si el caso lo exige, `1` o más tablas complementarias.
- `1` pipeline reproducible de preparación en `Python`.
- `1` workbook en `Tableau` con al menos `8` hojas analíticas útiles.
- `1` dashboard final integrado con al menos `3` bloques:
  - contexto y KPIs
  - exploración comparativa o segmentada
  - módulo temporal, comparativo o avanzado
- `1` historia visual breve con `3` a `5` pantallas o una secuencia narrativa equivalente.
- `1` vista longitudinal sólida.
- `1` vista transversal sólida.
- `1` componente avanzado integrado o anexado metodológicamente al análisis.
- `1` documento de QA con validación técnica, limitaciones y decisiones de diseño.

## Condiciones generales de evaluación

- Ninguna entrega parcial debe entenderse como un entregable aislado; cada una debe reutilizar, corregir y ampliar la anterior.
- No se debe presentar un dashboard visualmente pulido sin evidencia técnica de preparación, perfilado y validación.
- No se debe presentar un notebook extenso sin traducción clara a decisiones visuales en Tableau.
- Las decisiones metodológicas deben quedar justificadas, no solo ejecutadas.
- Todo insight importante debe estar respaldado por al menos una evidencia visual o tabular verificable.
- Si el equipo cambia de dataset o de pregunta analítica luego de la semana `4`, debe justificar el cambio formalmente.
- El componente avanzado no reemplaza el análisis base; lo complementa.

## Requisitos mínimos del dataset

Para asegurar que el proyecto cubra todos los temas del curso, el dataset debe cumplir, idealmente, con estas características:

- Mínimo `2,000` registros.
- Mínimo `10` a `12` variables útiles.
- Al menos `1` dimensión temporal.
- Al menos `1` dimensión categórica fuerte.
- Al menos `1` dimensión de segmentación o agrupación.
- Al menos `4` variables numéricas.
- Idealmente, una dimensión geográfica.
- Para el componente avanzado, de preferencia al menos `8` variables numéricas o una representación vectorial que permita usar `PCA` o `t-SNE`.

## Restricciones y criterios de aceptación del dataset

- Debe ser un dataset real, público, institucional o construido a partir de una fuente verificable.
- No se recomienda un dataset excesivamente pequeño o trivial.
- No se recomienda usar datasets extremadamente limpios si impiden trabajar perfilado y limpieza.
- El dataset debe permitir una historia analítica plausible.
- Debe existir claridad sobre:
  - origen
  - cobertura
  - periodo
  - limitaciones
  - licencia o permiso de uso

## Temas que el proyecto debe incluir obligatoriamente

### 1. Definición del problema y del usuario objetivo

El proyecto debe responder claramente:

- ¿Qué problema se quiere analizar?
- ¿Quién usará el dashboard?
- ¿Qué decisión podría apoyarse con el producto final?

### 2. Perfilado y gobierno mínimo del dato

Debe incluir:

- unidad de análisis
- granularidad
- diccionario de datos
- tipos de variables
- porcentaje de nulos
- cardinalidad
- observaciones de calidad
- trazabilidad de fuente

### 3. Limpieza y preparación de datos

Debe incluir:

- tratamiento de nulos
- homologación de categorías
- corrección de tipos
- control de duplicados
- bitácora de transformaciones

### 4. Modelado analítico

Debe incluir, si corresponde:

- joins o relationships
- validación de cardinalidad
- tabla de hechos y dimensiones o estructura equivalente
- validación de totales y métricas

### 5. Análisis exploratorio y selección de gráficos

Debe incluir:

- comparaciones categóricas
- distribuciones
- relaciones entre variables
- primeras hipótesis o hallazgos
- justificación de selección de gráficos

### 6. Segmentación e interpretación

Debe incluir:

- análisis por segmentos
- comparación entre subgrupos
- mínimo `3` insights bien redactados

### 7. Cálculos analíticos

Debe incluir:

- métricas derivadas
- porcentajes o participaciones
- acumulados o comparaciones relativas
- parámetros o filtros significativos en Tableau

### 8. Storytelling técnico

Debe incluir:

- una narrativa clara
- títulos analíticos
- anotaciones o énfasis visual
- recomendación final conectada con la evidencia

### 9. Accesibilidad y diseño

Debe incluir:

- contraste adecuado
- uso intencional del color
- jerarquía visual
- layout limpio
- revisión mínima de accesibilidad

### 10. Visualización longitudinal

Debe incluir al menos una vista temporal sólida que trabaje:

- tendencia
- variación
- comparación temporal
- posible suavizado o promedio móvil

### 11. Visualización transversal

Debe incluir al menos una vista comparativa transversal:

- por región
- por segmento
- por categoría
- por cohorte
- o por una estructura equivalente

### 12. Componente avanzado obligatorio

Se recomienda que este componente sea:

- `PCA`
- `t-SNE`

Si el dataset no permite usar estas técnicas de manera razonable, el equipo debe justificar una alternativa avanzada de complejidad equivalente, por ejemplo:

- clustering exploratorio
- embeddings ya disponibles
- reducción de dimensionalidad con `PCA` sobre variables derivadas
- análisis espacial con normalización robusta

### 13. Dashboard final publicable

Debe incluir:

- vista principal
- contexto analítico
- interactividad con sentido
- narrativa implícita o explícita
- preparación para publicación o demo

### 14. Defensa final

El equipo debe poder defender:

- la elección del problema
- la elección del dataset
- las decisiones de limpieza
- las decisiones de modelado
- la elección de gráficos
- las métricas construidas
- la validez de sus insights
- las limitaciones del análisis

## Estructura recomendada de entregas parciales

La idea es que el trabajo final no aparezca al final del curso como un producto improvisado, sino como una construcción progresiva.

### Entrega 1. Propuesta del proyecto

Semana sugerida: `3`

Contenido:

- tema del proyecto
- pregunta analítica principal
- usuario objetivo
- fuente de datos propuesta
- hipótesis iniciales
- justificación del valor del proyecto

Entregables:

- documento breve en `PDF`
- enlace o archivo del dataset
- mini ficha del proyecto

Criterios mínimos de aprobación:

- la pregunta analítica no es descriptiva trivial
- el usuario objetivo está claramente identificado
- el dataset tiene potencial real para temporalidad, segmentación y comparación
- se explicita por qué `Tableau` es adecuado para el caso
- se identifican riesgos iniciales de calidad o cobertura

Peso sugerido:

- `10%`

### Entrega 2. Perfilado, diccionario y limpieza inicial

Semana sugerida: `5`

Contenido:

- perfilado completo del dataset
- diccionario de datos
- identificación de problemas de calidad
- reglas de limpieza
- bitácora inicial
- modelado de datos

Entregables:

- notebook de perfilado y limpieza
- tabla de perfilado
- dataset limpio preliminar
- bitácora de transformaciones

Criterios mínimos de aprobación:

- se documenta la unidad de análisis
- se reportan nulos, cardinalidad, duplicados y campos críticos
- se registra al menos una decisión de limpieza por tipo de problema detectado
- el dataset limpio preliminar puede conectarse a Tableau sin ambigüedad de tipos
- la bitácora distingue entre dato original y dato transformado

Peso sugerido:

- `10%`

### Entrega 3. Análisis exploratorio y selección de gráficos

Semana sugerida: `7`

Contenido:

- primeras visualizaciones exploratorias
- comparación, distribución, relación y tendencia
- tabla de decisiones de gráficos
- primeros insights

Entregables:

- notebook exploratorio
- workbook preliminar en Tableau
- documento corto con `3` a `5` insights

Criterios mínimos de aprobación:

- se muestran vistas de comparación, distribución, relación y tiempo
- cada gráfico tiene una justificación técnica breve
- al menos `2` gráficos preliminares son descartados y se explica por qué
- los insights están redactados en lenguaje analítico, no solo descriptivo
- el workbook preliminar ya tiene una estructura navegable

Peso sugerido:

- `5%`

### Entrega 4. Modelado, métricas y dashboard alpha

Semana sugerida: `11`

Contenido:

- estructura analítica o relacional
- métricas derivadas
- segmentación
- parámetros o lógica analítica
- primera versión de dashboard funcional

Entregables:

- notebook de modelado y cálculos
- fuentes finales o semidefinitivas para Tableau
- dashboard alpha

Criterios mínimos de aprobación:

- la estructura relacional está validada y no duplica métricas sin control
- se implementan métricas derivadas consistentes con la pregunta del proyecto
- el dashboard alpha ya tiene flujo de lectura y filtros con sentido
- existe al menos una vista por segmento relevante
- el equipo puede explicar cómo cada cálculo afecta la interpretación

Peso sugerido:

- `10%`

### Entrega 5. Storytelling, accesibilidad y módulo temporal/comparativo

Semana sugerida: `13`

Contenido:

- rediseño de dashboard con foco narrativo
- mejora de accesibilidad
- vista longitudinal sólida
- vista transversal sólida

Entregables:

- dashboard revisado
- historia visual breve
- checklist de accesibilidad
- mini reflexión metodológica

Criterios mínimos de aprobación:

- el dashboard mejora respecto al alpha en jerarquía visual y legibilidad
- se valida contraste, uso de color, etiquetas y títulos analíticos
- se incluye una vista longitudinal y una transversal claramente defendibles
- la historia visual no repite gráficos sin aportar mensaje
- la reflexión metodológica reconoce límites y decisiones de diseño

Peso sugerido:

- `15%`

### Entrega 6. Trabajo final completo y defensa

Semana sugerida: `15`

Contenido:

- aplicación de `PCA`, `t-SNE` o alternativa aprobada
- integración del resultado al análisis
- documentación metodológica de la técnica
- versión beta final del dashboard
- dashboard final
- historia visual o secuencia de presentación
- QA técnico
- defensa del pipeline completo

Entregables:

- dashboard final en Tableau
- notebook final o carpeta de notebooks
- base final preparada
- presentación de defensa
- documento resumen ejecutivo

Criterios mínimos de aprobación:

- el dashboard final responde la pregunta principal sin depender de explicación externa extensa
- el pipeline técnico es reproducible y entendible
- el equipo evidencia cobertura de todo el curso
- la defensa muestra control de supuestos, límites y decisiones
- el producto final puede presentarse como pieza publicable o demo funcional

Peso sugerido:

- `15%`


## Relación directa con lo visto en clase

Este diseño de trabajo final integra explícitamente todo lo visto en el curso:

- perfilado y granularidad
- limpieza
- modelado
- chart selection
- análisis exploratorio
- segmentación
- cálculos analíticos
- storytelling
- accesibilidad
- series temporales
- comparación transversal
- mapas si el dataset lo permite
- `PCA` o `t-SNE`
- dashboard engineering
- defensa final

## Matriz de cobertura de contenidos por entrega

| Tema del curso | E1 | E2 | E3 | E4 | E5 | E6 | E7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Definición del problema | X |  |  |  |  |  | X |
| Selección y validación del dataset | X | X |  |  |  |  | X |
| Perfilado y granularidad |  | X |  |  |  |  | X |
| Limpieza y preparación |  | X | X | X |  |  | X |
| Modelado analítico |  |  |  | X |  |  | X |
| Exploración y chart selection |  |  | X | X |  |  | X |
| Segmentación e insights |  |  | X | X | X |  | X |
| Cálculos analíticos |  |  |  | X | X |  | X |
| Storytelling técnico |  |  |  | X | X |  | X |
| Accesibilidad y diseño |  |  |  |  | X |  | X |
| Visualización temporal |  |  | X | X | X |  | X |
| Visualización transversal |  |  | X | X | X | X | X |
| Componente avanzado |  |  |  |  |  | X | X |
| Dashboard engineering |  |  |  | X | X | X | X |
| Defensa metodológica |  |  |  |  |  |  | X |

## Recomendación sobre herramientas

### Obligatorio

- `Tableau`
- `Python`
- notebooks en `Jupyter`

### Recomendado

- `pandas`
- `matplotlib`
- `seaborn`
- `plotly`
- `scikit-learn`

### Opcional

- `Power BI` como comparación breve o anexo

## Propuesta de formato técnico de entrega

Se recomienda que cada equipo entregue una carpeta con esta estructura:

```text
proyecto-final/
  data/
  notebooks/
  outputs/
  tableau/
  docs/
  README.md
```

Contenido mínimo:

- `data/`: fuentes originales y limpias
- `notebooks/`: notebooks de trabajo
- `outputs/`: CSVs o tablas exportadas para Tableau
- `tableau/`: workbook o enlace publicado
- `docs/`: presentación, diccionario, bitácora, QA
- `README.md`: explicación general del proyecto

## Relación sugerida con los notebooks semanales del curso

Para mantener alineación entre teoría, laboratorio y proyecto, se recomienda mapear las entregas parciales con los notebooks del curso:

- Entrega `1`: [notebooks/semana-01-introduccion-tableau.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-01-introduccion-tableau.ipynb) y [notebooks/semana-02-perfilado-granularidad.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-02-perfilado-granularidad.ipynb)
- Entrega `2`: [notebooks/semana-03-limpieza-datos.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-03-limpieza-datos.ipynb) y [notebooks/semana-04-modelado-fuentes.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-04-modelado-fuentes.ipynb)
- Entrega `3`: [notebooks/semana-05-chart-selection.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-05-chart-selection.ipynb) y [notebooks/semana-06-segmentacion-insights.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-06-segmentacion-insights.ipynb)
- Entrega `4`: [notebooks/semana-07-calculos-lod-analogos.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-07-calculos-lod-analogos.ipynb) y [notebooks/semana-08-storytelling-anotacion.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-08-storytelling-anotacion.ipynb)
- Entrega `5`: [notebooks/semana-09-accesibilidad-diseno.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-09-accesibilidad-diseno.ipynb), [notebooks/semana-10-series-temporales.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-10-series-temporales.ipynb) y [notebooks/semana-11-comparacion-transversal-mapas.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-11-comparacion-transversal-mapas.ipynb)
- Entrega `6`: [notebooks/semana-12-pca-tsne.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-12-pca-tsne.ipynb)
- Entrega `7`: [notebooks/semana-13-dashboard-engineering.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-13-dashboard-engineering.ipynb) y [notebooks/semana-14-capstone-qa.ipynb](/Users/adrianalarcon/upc/master/computer_science/data-visualization/notebooks/semana-14-capstone-qa.ipynb)

## Variantes temáticas sugeridas

### Opción 1. Retail o e-commerce

Pregunta ejemplo:

- ¿Qué categorías, regiones y segmentos explican mejor la rentabilidad y la variación de ventas?

### Opción 2. Educación

Pregunta ejemplo:

- ¿Qué factores se asocian con rendimiento, permanencia o riesgo académico a lo largo del tiempo?

### Opción 3. Salud pública

Pregunta ejemplo:

- ¿Cómo cambian ciertos indicadores por región, tiempo y perfil poblacional?

### Opción 4. Movilidad o transporte

Pregunta ejemplo:

- ¿Qué patrones temporales y espaciales explican demanda, congestión o incidencias?

### Opción 5. Recursos humanos

Pregunta ejemplo:

- ¿Qué variables se asocian con rotación, desempeño o ausentismo por unidad y periodo?

## Recomendación final

La mejor versión de este trabajo final no es un dashboard lleno de gráficos, sino un producto con estas características:

- responde una pregunta real
- usa datos con trazabilidad
- documenta sus decisiones
- construye insights defendibles
- comunica con claridad
- y puede sostener técnicamente lo que afirma

## Sugerencia operativa adicional

Dado que ya se construyeron `slides` y `notebooks` por semana, una muy buena estrategia docente es exigir que cada entrega parcial se base directamente en el notebook correspondiente del curso.

Esto permite:

- alinear teoría y práctica
- evitar entregas improvisadas
- hacer retroalimentación incremental
- y construir el trabajo final como acumulación de evidencia, no como esfuerzo de último momento
