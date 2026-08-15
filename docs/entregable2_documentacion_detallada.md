# Entregable 2 - Documentacion detallada

## Proyecto

**Curso:** Data Visualization (1ACC0211) - UPC  
**Nombre del proyecto:** GlobalTradeAnalysis  
**Tema:** dinamica del comercio mundial: exportaciones e importaciones por pais, categoria de producto y region geografica (1989-2023)  
**Notebook principal:** [Entregable2_Perfilado_Limpieza_Consolidado.ipynb](../code/notebooks/Entregable2_Perfilado_Limpieza_Consolidado.ipynb)

## Proposito de este documento

Este documento explica de manera completa lo que se hizo en la Entrega 2, desde la lectura del dataset original hasta la generacion del dataset limpio listo para Tableau.

La idea es que una persona que no conoce el proyecto pueda entender:

- que contiene el dataset original
- por que se tuvo que perfilar antes de limpiar
- que problemas de calidad se encontraron
- como se tomo cada decision de limpieza
- por que algunas filas se eliminaron y otras no
- por que se crearon columnas nuevas
- que archivo final se debe usar para el analisis

## 1. Resumen ejecutivo

La Entrega 2 tuvo como objetivo transformar un dataset historico de comercio internacional en una base limpia, trazable y util para analisis en Tableau.

El dataset original mezcla varias capas de informacion:

- paises y territorios vigentes
- entidades historicas que ya no existen
- agregados regionales y globales
- variables comerciales
- variables arancelarias
- indicadores de crecimiento
- columnas redundantes o constantes

Por esa razon, no era suficiente con "borrar nulos". Primero fue necesario entender la estructura real del archivo, documentar la calidad de cada variable y luego aplicar una limpieza con criterio analitico.

## 2. Archivos involucrados

### Entrada

- [34_years_world_export_import_dataset.csv](../data/raw/34_years_world_export_import_dataset.csv)

### Salidas generadas por el notebook

- [dataset_limpio_entrega2_consolidado.csv](../data/processed/dataset_limpio_entrega2_consolidado.csv)
- [dataset_agregados_referencia.csv](../data/processed/dataset_agregados_referencia.csv)
- [tabla_perfilado_entrega2_consolidado.csv](../data/processed/tabla_perfilado_entrega2_consolidado.csv)
- [bitacora_transformaciones_entrega2_consolidado.csv](../data/processed/bitacora_transformaciones_entrega2_consolidado.csv)

## 3. Que representa el dataset original

El archivo original contiene informacion de comercio exterior para paises y territorios durante varios anios.

Cada fila representa, en principio, un pais o territorio en un anio dado. Por eso la unidad de analisis correcta es:

- **Unidad de analisis:** pais x anio
- **Granularidad:** anual

Eso significa que una fila no es una transaccion individual, sino un resumen anual por territorio.

### Variables principales

El archivo contiene tres tipos de columnas:

- **Identificacion:** `Partner Name`, `Year`
- **Comercio:** exportaciones, importaciones y balances
- **Aranceles:** indicadores AHS y MFN
- **Crecimiento:** `World Growth (%)` y `Country Growth (%)`
- **Columnas de control o referencia:** shares, RCA y min rates

## 4. Primer perfilado del dataset

Antes de limpiar, se realizo un perfilado general para responder preguntas basicas:

- cuantas filas y columnas hay
- que tipos de datos tiene cada columna
- cuantos nulos hay por variable
- cual es la cardinalidad de los campos categorizos o identificadores
- si hay duplicados en la clave natural

### Hallazgos iniciales

1. El dataset tiene una estructura historica real, pero no completa para todas las combinaciones pais x anio.
2. No todos los territorios tienen la misma cobertura temporal.
3. Existen columnas que no agregan valor analitico porque son constantes o redundantes.
4. Hay filas que representan agregados regionales y no paises individuales.
5. Hay entidades historicas que ya no existen, pero que deben conservarse como parte del contexto historico.

## 5. Lógica de la limpieza

La limpieza no se hizo de forma mecanica. Se aplico una logica de negocio y una logica analitica.

La regla general fue esta:

- conservar lo que ayuda a explicar el fenomeno
- eliminar lo que no aporta variacion ni analisis
- etiquetar lo historico en lugar de destruirlo
- separar lo agregado de lo individual
- dejar trazabilidad de cada cambio

## 6. Decisiones de limpieza explicadas en detalle

### 6.1 Homologacion de nombres de paises

**Problema:** algunos nombres de paises tenian espacios extra al inicio o al final.

**Accion:** se aplico `str.strip()` sobre `Partner Name`.

**Por que se hizo:**

Los espacios invisibles generan errores en filtros, joins, comparaciones y agrupaciones. Dos textos que parecen iguales pueden ser tratados como diferentes por el sistema. Esa clase de problema es muy comun y no se ve a simple vista.

**Resultado esperado:**

- nombres uniformes
- menos riesgo de duplicados falsos
- mejor consistencia para Tableau y para futuras relaciones con otras tablas

### 6.2 Separacion de agregados regionales

**Problema:** el dataset mezcla paises con agregados como `World` y regiones geograficas como `Europe & Central Asia`.

**Accion:** esas filas se separaron del dataset analitico y se guardaron en `df_agregados`.

**Por que se hizo:**

Un agregado regional no es comparable con un pais individual. Si se mezclan ambos niveles de analisis, se distorsionan las comparaciones, los promedios y los rankings.

Por ejemplo:

- `World` no debe competir con `Peru`
- `North America` no debe analizarse como si fuera un pais
- una region resume varias economias a la vez

**Decision metodologica:**

- el dataset limpio contiene solo unidades analiticas comparables
- el archivo de agregados se conserva para trazabilidad y referencia

### 6.3 Clasificacion de entidades historicas

**Problema:** aparecen territorios que ya no existen como estados politicos vigentes, por ejemplo:

- Soviet Union
- Czechoslovakia
- German Democratic Republic
- Yugoslavia
- Yemen Democratic

**Accion:** se creo la columna `entity_status` con dos categorias:

- `Activo`
- `Extinto`

**Por que no se eliminaron:**

Porque forman parte del periodo historico cubierto por el dataset. Borrarlos haria perder contexto y distorsionaria la lectura del pasado.

**Logica detras de la decision:**

- no son errores de datos
- no son paises mal escritos
- representan entidades historicas validas para el periodo analizado
- deben conservarse para analisis narrativo o contextual

**Criterio final:**

Se conservan, pero se etiquetan. Eso permite diferenciarlos sin perder la historia.

### 6.4 Exclusion de territorios con cobertura insuficiente

**Problema:** algunos territorios tienen muy pocos anios de datos.

**Accion:** se excluyeron del dataset analitico los territorios no extintos con menos de 10 observaciones anuales.

**Por que se hizo:**

Cuando una entidad tiene muy pocos registros, no permite una comparacion temporal seria. En analisis longitudinales, una cobertura demasiado corta puede producir interpretaciones erroneas.

**Criterio aplicado:**

- si la cobertura es baja y el territorio no es historico extinto, se excluye
- si la entidad es historica extinta, no se excluye solo por tener poca cobertura

**Logica detras de la decision:**

No todos los huecos significan error. Algunos huecos son historicamente correctos. Por eso la regla no fue ciega, sino condicionada por el tipo de entidad.

### 6.5 Reconstruccion de `World Growth (%)`

**Problema:** `World Growth (%)` tiene nulos, pero en realidad ese valor deberia ser el mismo para todos los paises de un mismo anio.

**Accion:** se reconstruyo por anio usando el primer valor no nulo de cada año y se distribuyo a todas las filas del mismo anio.

**Por que se hizo:**

Este campo no es una caracteristica propia de cada pais, sino una referencia global por anio. Si un valor esta disponible para una fila del anio, puede replicarse a las demas filas del mismo anio.

**Logica detras de la decision:**

- el valor es temporal, no territorial
- por eso debe repetirse por anio
- completar por anio es coherente con la naturaleza de la variable

### 6.6 Imputacion de nulos pequenos en variables AHS y MFN

**Problema:** varias variables arancelarias tienen pocos nulos, en torno a fracciones del 1%.

**Accion:** se imputaron con la mediana del mismo anio.

**Por que se hizo:**

La mediana es una medida robusta. A diferencia del promedio, no se altera tanto por valores extremos. Eso la hace adecuada cuando hay pocos datos faltantes y la distribucion puede ser asimetrica.

**Logica detras de la decision:**

- no habia suficiente razon para eliminar filas enteras por unos pocos nulos
- rellenar con la mediana preserva el registro
- usar la mediana por anio respeta el contexto temporal

**Importante:**

No se imputaron variables que no lo necesitaban ni se inventaron valores donde no habia una regla clara.

### 6.7 Marcas para exportaciones en cero

**Problema:** algunas filas tienen exportaciones igual a cero.

**Accion:** se creo una bandera `flag_export_cero`.

**Por que se hizo:**

Un valor cero en comercio exterior puede significar varias cosas:

- ausencia real de exportacion
- dato faltante codificado como cero
- cobertura limitada o caso especial

En lugar de asumir una sola interpretacion, se marca el caso para no perder la informacion.

**Logica detras de la decision:**

- el cero es una señal que merece seguimiento
- eliminar la fila puede ser demasiado agresivo
- marcar la fila permite estudiar el patron sin destruir el dato original

### 6.8 Marca para valores extremos en `MFN AVE`

**Problema:** la columna `MFN AVE Tariff Lines Share (%)` puede superar 100.

**Accion:** se creo la bandera `flag_mfn_ave_extremo`.

**Por que se hizo:**

Esto no necesariamente es un error. En comercio y aranceles, ciertas tasas equivalentes ad valorem pueden generar valores altos por la forma en que se calculan. Por eso no se elimino automaticamente.

**Logica detras de la decision:**

- un valor alto no siempre es invalido
- puede corresponder a una definicion tecnica legitima
- conviene marcarlo para visualizacion o analisis de outliers

### 6.9 Eliminacion de columnas constantes o redundantes

**Columnas eliminadas:**

- `Export Product Share (%)`
- `Import Product Share (%)`
- `Revealed comparative advantage`
- `MFN MinRate (%)`
- `Country Growth (%)`

**Por que se eliminaron:**

Porque no aportaban variacion analitica suficiente o duplicaban informacion ya representada en otra variable.

#### Explicacion de cada caso

- `Export Product Share (%)`: se comporta como una constante, por lo tanto no ayuda a discriminar entre paises o anios.
- `Import Product Share (%)`: tambien es constante y no agrega variacion.
- `Revealed comparative advantage`: todos los valores no nulos son 1.0, por lo tanto no sirve para comparar.
- `MFN MinRate (%)`: es constante y no agrega informacion util.
- `Country Growth (%)`: resulto redundante con `World Growth (%)` en la logica de trabajo del notebook y no aportaba una lectura distinta.

**Logica detras de la decision:**

Cuando una variable no cambia o no explica nada nuevo, solo agrega ruido. En un dashboard, el ruido hace mas dificil interpretar el mensaje.

### 6.10 Creacion de variables derivadas

Se crearon nuevas columnas para enriquecer el analisis:

- `Export (US$ Million)`
- `Import (US$ Million)`
- `Trade Balance (US$ Thousand)`
- `Trade Balance (US$ Million)`
- `Total Trade (US$ Thousand)`
- `Total Trade (US$ Million)`
- `Trade Status`

**Por que se hicieron:**

Las variables derivadas resumen relaciones importantes que no estaban explicitadas en el dataset original.

#### Significado de cada una

- `Trade Balance`: exportaciones menos importaciones
- `Total Trade`: exportaciones mas importaciones
- valores en millones: facilitan lectura en visualizaciones
- `Trade Status`: clasifica el resultado en `Superavit`, `Deficit` o `Equilibrio`

**Logica detras de la decision:**

No basta con guardar los datos originales. Tambien hay que construir variables que ayuden a responder preguntas analiticas de manera mas directa.

### 6.11 Correccion final de tipos y ordenamiento

**Accion:**

- `Year` se conviertio a entero
- el dataset se ordeno por `Partner Name` y `Year`

**Por que se hizo:**

Esto mejora la lectura, la exportacion y la consistencia para herramientas como Tableau.

**Logica detras de la decision:**

- el año no debe tratarse como texto
- un orden estable facilita revisiones y series temporales
- el dataset queda listo para consumo analitico

## 7. Bitacora de transformaciones

La bitacora es una parte central del trabajo porque documenta cada decision de limpieza.

No solo dice que se cambio, sino tambien:

- por que se cambio
- que tipo de problema se resolvio
- que impacto tuvo
- si se eliminó, imputó, etiquetó o derivó informacion

### Por que es importante

La limpieza de datos no debe verse como un proceso oculto. Debe ser auditable.

La bitacora permite responder preguntas como:

- que se elimino
- que se imputo
- que se conservó
- que se etiquetó
- que quedo disponible para referencia

### Tipos de decisiones registradas

- eliminacion de columnas
- separacion de agregados regionales
- exclusion por baja cobertura
- clasificacion historica
- imputacion temporal
- banderas de control
- derivacion de nuevas metricas
- ordenamiento final

## 8. Dataset limpio final

El dataset limpio es la version que debe usarse para el analisis principal y para la conexion con Tableau.

### Caracteristicas finales

- contiene solo unidades analiticas comparables
- elimina columnas sin valor analitico
- conserva entidades historicas etiquetadas
- mantiene trazabilidad de los agregados separados
- agrega banderas y variables utiles para visualizacion

### Validaciones realizadas

Se verifico que el dataset final:

- no tenga duplicados en `Partner Name` + `Year`
- tenga tipos consistentes
- tenga variables criticas completas o tratadas correctamente
- sea compatible con Tableau

## 9. Archivo de agregados de referencia

El archivo `dataset_agregados_referencia.csv` existe para no perder las filas de `World` y regiones.

### Que contiene

- agregados globales
- regiones supranacionales

### Para que sirve

- auditoria
- trazabilidad
- comparacion documental
- referencia historica

### Para que no sirve

- no debe usarse como base del analisis principal
- no debe mezclarse con paises individuales en rankings o comparaciones directas

## 10. Logica general de las decisiones

El principio rector de toda la limpieza fue este:

> conservar la verdad historica del dato, pero convertirlo en una estructura analitica coherente.

Eso implico tres ideas:

1. **Lo historico se conserva** cuando tiene sentido contextual.
2. **Lo redundante se elimina** cuando no aporta variacion.
3. **Lo ambiguo se marca** cuando puede ser util pero necesita interpretacion.

## 11. Que debe usar una persona que empiece de cero

Si alguien quiere entender el proyecto desde cero, el recorrido recomendado es este:

1. leer este documento
2. abrir el notebook consolidado
3. revisar el perfilado del dataset
4. entender los hallazgos de calidad
5. revisar cada regla de limpieza una por una
6. inspeccionar la bitacora
7. usar el dataset limpio para Tableau

## 12. Que se aprendio con esta entrega

Esta entrega deja varias lecciones importantes:

- un dataset historico no debe limpiarse como si fuera una tabla simple
- los agregados regionales necesitan tratamiento distinto al de los paises
- las entidades historicas no son errores, son parte del contexto
- los nulos pueden tener causas distintas y no siempre se resuelven igual
- una buena limpieza necesita explicacion, no solo ejecucion

## 13. Relacion con el resto del proyecto

Esta entrega es la base tecnica para la siguiente etapa.

A partir del dataset limpio se puede avanzar a:

- analisis exploratorio
- seleccion de graficos
- storytelling
- dashboard en Tableau
- comparaciones longitudinales y transversales
- componente avanzado

## 14. Conclusion final

La Entrega 2 no consistio solo en "limpiar datos". Consistio en transformar un dataset historico complejo en una base interpretable, consistente y lista para analisis visual.

La limpieza se hizo con criterio porque cada decision responde a una pregunta concreta:

- esto aporta o no aporta analisis
- esto representa un pais o un agregado
- esto es un error o es historia
- esto se elimina, se marca o se conserva

Esa es la logica que sostiene todo el notebook consolidado y la que permite que la siguiente fase del proyecto parta desde una base solida.
