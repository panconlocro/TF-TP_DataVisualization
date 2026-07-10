# Justificación Analítica del Dashboard
## "Comercio mundial 1988–2021 — ¿Qué economías concentran las exportaciones y dónde está el riesgo de desbalance comercial?"

Este documento explica cómo cada componente del dashboard (KPIs, gráficos e insights) responde a la pregunta analítica principal, y por qué fue seleccionado.

---

## 1. Pregunta analítica principal

> ¿Qué economías concentran las exportaciones mundiales y dónde está el riesgo de desbalance comercial?

La pregunta tiene dos partes explícitas ("qué economías concentran" / "dónde está el riesgo") y admite un tercer eje implícito que refuerza la interpretación: **por qué ocurre ese patrón**. El dashboard está diseñado para responder las dos partes explícitas con evidencia visual directa, y complementarlas con el eje explicativo.

---

## 2. Rango temporal: justificación de 1988–2021

El dashboard cubre 34 años continuos de comercio mundial. Este rango no es arbitrario: captura tres shocks económicos completos y comparables —la crisis asiática de 1997, la Gran Recesión de 2009 (-22.9% interanual en exportaciones) y la recuperación post-pandemia de 2021 (+26.8% interanual)—, lo que permite un análisis longitudinal robusto de cómo el comercio global absorbe y se recupera de crisis de distinta naturaleza. El corte en 2021 corresponde al último año disponible en la fuente de datos al momento del análisis.

---

## 3. Bloque de KPIs (contexto)

| KPI | Valor 2021 | Rol analítico | Conexión con la pregunta |
|---|---|---|---|
| Exportaciones mundiales | $21,933,842M (+26.8% vs 2020) | Ancla de escala: dimensiona el tamaño del comercio mundial antes de segmentarlo | Da contexto necesario para interpretar los porcentajes de concentración y déficit que siguen |
| Concentración Tier 1 | 79.3% (29 de 238 países) | Responde directamente la primera mitad de la pregunta | **Responde "qué economías concentran"** |
| % Déficit Top 5 | 65.1% (vs año anterior -0.5%) | Responde directamente la segunda mitad de la pregunta | **Responde "dónde está el riesgo"** |
| Arancel AHS 2021 | 3.73% (vs 2020 +0.15pp) | Introduce el eje explicativo (por qué ocurre el patrón) | Prepara la lectura del Insight 3 y el dot plot de aranceles |

Los cuatro KPIs fueron seleccionados para que cada uno tenga función distinta (escala, concentración, riesgo, explicación) y ninguno sea redundante entre sí. Se descartó un KPI genérico de "Balance comercial total" porque, al ser un agregado global, no aportaba información sobre *dónde* se concentra el desbalance —justo lo que pregunta el dashboard—, y fue reemplazado por el KPI de % Déficit Top 5.

---

## 4. Gráficos y su rol en responder la pregunta

### 4.1 Línea temporal — Exportación e Importación 1988–2021
**Título:** "El comercio mundial se duplicó tras 2001 y rebotó +26.8% en 2021"

**Qué responde:** No responde directamente ninguna de las dos mitades de la pregunta, pero establece el contexto temporal indispensable para interpretarlas —muestra que 2021 es un año de rebote fuerte tras una caída (2009) y una posible disrupción (pandemia), lo cual matiza cómo se deben leer los KPIs y el resto de gráficos, que están anclados en ese mismo año.

**Por qué este tipo de gráfico:** una vista longitudinal (línea) es la forma estándar de mostrar tendencia, variación interanual y quiebres estructurales a lo largo de 34 años; ninguna otra forma de gráfico comunica evolución temporal con la misma claridad.

**Vista longitudinal del proyecto:** cumple el requisito de tendencia, variación (anotaciones de -22.9% y +26.8%) y comparación temporal (export vs import).

### 4.2 Barras horizontales — Líderes exportadores por período
**Título:** "29 países concentran el 79.3% de las exportaciones mundiales"

**Qué responde:** **Responde directamente "qué economías concentran las exportaciones"**, mostrando el ranking explícito de países por volumen exportado acumulado.

**Por qué este tipo de gráfico:** un ranking de magnitudes entre categorías (países) se lee mejor en barras horizontales ordenadas que en cualquier otra forma —permite comparar directamente la longitud de cada barra sin necesidad de leer etiquetas numéricas.

**Vista transversal del proyecto:** compara categorías (países) en un mismo corte, cumpliendo el requisito de comparación transversal.

### 4.3 Barras divergentes — Balance comercial por país (Exportación − Importación)
**Título:** "El déficit comercial se concentra en economías avanzadas: EE.UU. explica el 63% del Top 5 deficitario"

**Qué responde:** **Responde directamente "dónde está el riesgo de desbalance comercial"**, mostrando qué países tienen mayor déficit (rojo) y cuáles mayor superávit (verde/teal), ordenados de mayor a menor balance.

**Por qué este tipo de gráfico:** barras divergentes son la forma estándar para mostrar valores que se dividen naturalmente en dos polos (superávit/déficit) alrededor de un punto cero; permiten identificar de un vistazo tanto la magnitud como la dirección del desbalance, algo que un scatter o una tabla no comunican con la misma inmediatez.

**Nota de decisión metodológica:** inicialmente se evaluó un scatter plot (export vs. import, escala logarítmica, ~200 países) que contenía la misma información, pero fue descartado por dificultar la lectura a un usuario no técnico (saturación de puntos, escala logarítmica poco intuitiva, ausencia de ranking claro). Se optó por barras divergentes filtradas al Top 20 de países por comercio total, priorizando comunicación clara sobre exhaustividad.

**Vista transversal del proyecto:** segunda vista comparativa transversal, complementaria a la de exportadores.

### 4.4 Dot plot — Aranceles por tier de países exportadores
**Título:** "El liderazgo exportador no depende de bajos aranceles"

**Qué responde:** No responde ninguna de las dos mitades literales de la pregunta, sino el eje explicativo implícito: *por qué* ocurre el patrón de concentración observado en 4.2. Refuerza la recomendación final del dashboard (priorizar infraestructura logística sobre desregulación arancelaria).

**Por qué este tipo de gráfico:** un dot plot permite comparar un promedio ponderado (arancel) entre pocos grupos (3 tiers) contra una referencia (línea de promedio global), siendo más limpio que barras cuando el número de categorías es bajo y lo relevante es la posición relativa al promedio, no la magnitud absoluta.

---

## 5. Los tres insights: cómo cada uno cierra el argumento

Cada insight sigue la estructura **Verbo + métrica + segmento + comparación + implicancia**, y está respaldado por evidencia visual verificable en un gráfico específico del dashboard (no son afirmaciones sueltas).

### Insight 1 — Concentración de exportadores
> El comercio mundial concentra 79.3% de las exportaciones acumuladas 1988-2021 en solo 29 países (Tier 1), liderados por Estados Unidos (55.4 billones) que duplica a China (28.3 billones), mientras 180 países (Tier 3) apenas suman 5.1%. Priorizar alianzas logísticas de largo plazo con las economías Tier 1 y cobertura estratégica hacia mercados Tier 2 para reducir la dependencia de pocos ejes comerciales.

**Evidencia visual:** gráfico 4.2 (barras de líderes exportadores) + KPI de Concentración Tier 1.
**Responde:** primera mitad de la pregunta principal.

### Insight 2 — Riesgo de desbalance
> El déficit comercial 2021 se concentra en 5 economías avanzadas (Estados Unidos, Reino Unido, Suiza, Países Bajos y Francia), que explican 65.1% del desbalance mundial, liderado por EE.UU. (-$1,587,781M). Monitorear la dependencia comercial de estas economías como señal temprana de tensiones o ajustes en política arancelaria.

**Evidencia visual:** gráfico 4.3 (barras divergentes de balance) + KPI de % Déficit Top 5.
**Responde:** segunda mitad de la pregunta principal.

### Insight 3 — Arancel vs. competitividad
> Los exportadores Tier 1 sostienen un arancel promedio de 4.72%, por encima del promedio global de 3.72%, mientras Tier 3 opera por debajo del promedio (~3.5%). Esto evidencia que el liderazgo exportador no depende de baja protección arancelaria; descartar la reducción agresiva de aranceles como palanca de competitividad y priorizar inversión en infraestructura logística.

**Evidencia visual:** gráfico 4.4 (dot plot de aranceles) + KPI de Arancel AHS.
**Responde:** eje explicativo complementario (el "por qué"), que refuerza y da profundidad a los dos hallazgos anteriores sin ser parte literal de la pregunta.

---

## 6. Síntesis: matriz de cobertura

| Componente de la pregunta | KPI | Gráfico | Insight |
|---|---|---|---|
| "Qué economías concentran las exportaciones" | Concentración Tier 1 | Barras de líderes exportadores | Insight 1 |
| "Dónde está el riesgo de desbalance" | % Déficit Top 5 | Barras divergentes de balance | Insight 2 |
| "Por qué ocurre" (eje explicativo, no literal en la pregunta pero refuerza la recomendación) | Arancel AHS 2021 | Dot plot de aranceles | Insight 3 |

**Conclusión:** las dos partes literales de la pregunta principal están respondidas con evidencia visual directa (KPI + gráfico + insight cada una), no solo con texto descriptivo. El tercer eje (aranceles) no es parte literal de la pregunta pero fue incluido deliberadamente para explicar el mecanismo detrás del patrón observado, fortaleciendo la recomendación final del dashboard sin desviarse del alcance definido.