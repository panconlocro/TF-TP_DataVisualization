# Entrega 6 — Componente avanzado: PCA y t-SNE

**Curso:** Data Visualization (1ACC0211) — UPC
**Tema:** Dinámica del comercio mundial (1988–2021)

## 1. Objetivo y elección de la técnica

El componente avanzado aplica **PCA** (reducción de dimensionalidad) y **t-SNE** (proyección no
lineal) para responder una pregunta que las vistas base no abordan:

> ¿Existe un "perfil arancelario" que agrupe a los países, y ese perfil se relaciona con su
> tamaño exportador (Tier)?

**Por qué sobre las variables arancelarias y NO sobre el volumen.** El dataset tiene ~14
variables arancelarias numéricas (AHS/MFN: promedios, participaciones de líneas gravadas/libres,
específicas/ad-valorem, tasas máximas), altamente colineales — el caso de libro para PCA. En
cambio, aplicar PCA sobre las variables de volumen (Export, Import, Total Trade) sería
**circular**: todas son "tamaño" y el `Export_Tier` se definió justamente a partir del volumen,
por lo que el PCA solo redescubriría la variable que ya usamos para segmentar. Reducir el perfil
arancelario es independiente de cómo se construyó el Tier, por lo que el análisis es válido.

Esto además cierra un hilo de la Entrega 3: allí se descartó el *pairplot* de 23 variables
arancelarias por su colinealidad (descarte D02); PCA es la solución metodológicamente correcta a
ese mismo problema.

## 2. Preparación de datos

- **Unidad:** un país (corte 2021), un vector de 14 variables arancelarias en %.
- **Exclusiones:** agregados que no son países (`Unspecified`, `Special Categories`,
  `Free Zones`, `Other Asia, nes`) y columnas con varianza cero.
- **Estandarización:** `StandardScaler` (media 0, desviación 1), imprescindible antes de PCA.
- **Cobertura resultante:** 234 países con perfil arancelario completo.

## 3. Resultados del PCA

| Componente | Varianza explicada | Acumulada |
|---|---|---|
| PC1 | 24.8% | 24.8% |
| PC2 | 19.9% | 44.7% |
| PC3 | 14.7% | 59.5% |

Interpretación de las cargas (loadings):

- **PC1 ≈ nivel de protección**: dominado por `AHS Dutiable/Duty Free Tariff Lines Share`,
  `AHS Simple Average` y `MFN MaxRate` — separa países con muchas líneas gravadas de los de
  mercado más abierto.
- **PC2 ≈ estructura del arancel**: dominado por `MFN Specific/AVE Tariff Lines Share`,
  `AHS Weighted Average` y `AHS MaxRate` — distingue aranceles específicos de ad-valorem.

## 4. Relación con el tamaño exportador (Tier) — el hallazgo

Al proyectar en 2D y colorear por `Export_Tier`, **los tiers no se separan**:

| Tier | Media de PC1 |
|---|---|
| Tier 1 — Grandes Exportadores | −0.05 |
| Tier 2 — Exportadores Medianos | −0.30 |
| Tier 3 — Exportadores Pequeños | +0.08 |

Un clustering k-means (k=3) sobre el mismo perfil tampoco recupera los tiers: los grupos están
dominados por la cola de países pequeños y mezclan tiers; solo se aísla un outlier degenerado
(*Br. Antr. Terr.*).

**Insight (multivariado y no circular):**
> El perfil arancelario de un país es **independiente de su tamaño exportador**: grandes y
> pequeños exportadores no forman grupos arancelarios distintos. Esto refuerza, desde un enfoque
> multivariado, el hallazgo del dot plot (G3): el arancel no explica la capacidad exportadora;
> pesan más factores como la escala productiva y la estructura de la economía.

## 5. t-SNE

Se ejecutó t-SNE (perplexity = 15, `init="pca"`, `random_state=42`) sobre el mismo perfil
estandarizado, como validación no lineal. El resultado es consistente con el PCA: no aparecen
clusters nítidos alineados con el Tier. (t-SNE preserva estructura local, no distancias globales;
no se interpretan las distancias entre grupos lejanos.)

## 6. Limitaciones (control de supuestos)

- **PC1+PC2 explican solo 44.7%** de la varianza: la proyección 2D es un resumen aproximado; más
  de la mitad de la información vive en dimensiones superiores. El espacio arancelario es
  genuinamente multidimensional, por lo que las conclusiones se plantean como tendencia, no como
  separación limpia.
- El corte 2021 puede tener sesgo por cobertura de reporte arancelario de algunos países.
- t-SNE es exploratorio y sensible a la perplexity; se usa como apoyo, no como prueba.

## 7. Integración a Tableau

Se exportan las coordenadas (`PC1`, `PC2`, `tsne_x`, `tsne_y`, `cluster`, `Export_Tier`) a un CSV;
en Tableau se construye un **scatter coloreado por Tier**, integrando el componente avanzado al
dashboard en lugar de dejarlo aislado.

## 8. Código reproducible

```python
import pandas as pd, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

df   = pd.read_csv("data/processed/dataset_limpio_entrega2_consolidado.csv", encoding="utf-8-sig")
dimc = pd.read_csv("outputs/tableau_sources/Dim_Country.csv")
tiers = dict(zip(dimc["Partner Name"], dimc["Export_Tier"]))

# 14 variables de perfil arancelario (en %, sin las de importaciones en US$)
tar = [c for c in df.columns if ("AHS" in c or "MFN" in c) and "%" in c and "Imports" not in c]
no_pais = ["Unspecified", "Special Categories", "Free Zones", "Other Asia, nes"]
d = df[(df.Year == 2021) & (~df["Partner Name"].isin(no_pais))].dropna(subset=tar).copy()
tar = [c for c in tar if d[c].std() > 0]                     # quitar columnas constantes

X = StandardScaler().fit_transform(d[tar])                   # estandarizar

pca = PCA().fit(X)
print("Varianza explicada:", np.round(pca.explained_variance_ratio_[:5], 3))

d[["PC1", "PC2"]]     = PCA(n_components=2).fit_transform(X)
d[["tsne_x","tsne_y"]] = TSNE(perplexity=15, random_state=42, init="pca").fit_transform(X)
d["cluster"]          = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(X)
d["Export_Tier"]      = d["Partner Name"].map(tiers)

d[["Partner Name","Export_Tier","PC1","PC2","tsne_x","tsne_y","cluster"]] \
    .to_csv("outputs/tableau_sources/PCA_tSNE_Paises.csv", index=False)
```
