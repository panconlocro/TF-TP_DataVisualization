# GlobalTradeAnalysis

Análisis de la dinámica del comercio mundial (1989–2023): exportaciones e importaciones por país y región geográfica.

**Curso:** Data Visualization (1ACC0211) — Universidad Peruana de Ciencias Aplicadas

**Proyecto:** GlobalTradeAnalysis — análisis de la dinámica del comercio mundial: exportaciones e importaciones por país y región geográfica.

| Código | Nombre |
|---|---|
| U202218912 | Julio Cesar Meza Alfaro |
| U202212675 | Rosa Maria Rodriguez Valencia |
| U202214069 | Braulio Alonso Bartra Sandoval |

---

## Cómo ejecutar el proyecto

### Requisitos

```bash
pip install -r requirements.txt
```

---

### Paso 1 — Ingesta del dataset

```bash
python scripts/ingest.py
```

Descarga el dataset desde Kaggle y lo guarda en `data/raw/`.  
> Requiere credenciales de Kaggle configuradas con `kagglehub`.

---

### Paso 2 — Entrega 2: Perfilado y limpieza

Abre y ejecuta (Run All):

```
notebooks/entrega2-perfilado-limpieza.ipynb
```

**Genera:**
- `data/processed/dataset_limpio_entrega2_consolidado.csv` ← input de los pasos siguientes
- `data/processed/tabla_perfilado_entrega2_consolidado.csv`
- `data/processed/bitacora_transformaciones_entrega2_consolidado.csv`

---

### Paso 3 — Entrega 3: Modelado y benchmarking

Abre y ejecuta (Run All):

```
notebooks/entrega3-pipeline-final.ipynb
```

**Genera:**
- `outputs/tabla_comparativa_modelos.csv`
- `outputs/tableau_sources/Fact_Trade.csv`
- `outputs/tableau_sources/Dim_Country.csv`
- `outputs/tableau_sources/Dim_Time.csv`

---

### Paso 4 — Análisis exploratorio y selección de gráficos

Abre y ejecuta (Run All):

```
notebooks/entrega3-analisis-exploratorio.ipynb
```

Produce las 8 visualizaciones exploratorias (V01–V08) con justificación técnica y documenta los gráficos descartados (D01–D03).

---

## Estructura del proyecto

```
├── notebooks/
│   ├── entrega2-perfilado-limpieza.ipynb         # Paso 2: limpieza y perfilado del dataset
│   ├── entrega3-pipeline-final.ipynb             # Paso 3: modelado dimensional y benchmarking
│   ├── entrega3-analisis-exploratorio.ipynb      # Paso 4: visualizaciones exploratorias
│   └── _borradores/                              # Drafts anteriores (no ejecutar)
│
├── scripts/
│   └── ingest.py                                 # Paso 1: descarga el dataset desde Kaggle
│
├── data/
│   ├── raw/
│   │   └── 34_years_world_export_import_dataset.csv   # Dataset original
│   └── processed/
│       ├── dataset_limpio_entrega2_consolidado.csv    # Dataset limpio ← INPUT principal
│       ├── tabla_perfilado_entrega2_consolidado.csv
│       ├── bitacora_transformaciones_entrega2_consolidado.csv
│       └── dataset_agregados_referencia.csv
│
├── docs/
│   ├── entrega3-reporte-modelado.md              # Reporte de métricas y decisión del modelo
│   ├── entrega3-analisis-exploratorio.md         # Documentación escrita de visualizaciones
│   ├── entregable2_documentacion_detallada.md    # Documentación Entrega 2
│   └── propuesta-trabajo-final-con-entregas-parciales.md
│
├── outputs/
│   ├── tabla_comparativa_modelos.csv             # Tabla comparativa generada por el notebook
│   └── tableau_sources/
│       ├── Fact_Trade.csv                        # Para Tableau
│       ├── Dim_Country.csv                       # Para Tableau
│       └── Dim_Time.csv                          # Para Tableau
│
├── requirements.txt
└── setup.ps1
```

---

## Entregables Entrega 3

| Entregable | Archivo |
|---|---|
| Notebook de preprocesamiento y modelado | `notebooks/entrega3-pipeline-final.ipynb` |
| Tabla comparativa de opciones de modelo | `outputs/tabla_comparativa_modelos.csv` |
| Reporte de métricas y decisión | `docs/entrega3-reporte-modelado.md` |

---

## Modelo seleccionado

**Esquema en Estrella** — tres tablas conectadas en Tableau mediante *Relationships*:

```
Fact_Trade ──► Dim_Country   (252 países — surrogate key int64)
           ──► Dim_Time      (34 años + World Growth % — surrogate key int64)
```

La justificación empírica completa está en `docs/entrega3-reporte-modelado.md` y en la Sección 6 del notebook principal.
