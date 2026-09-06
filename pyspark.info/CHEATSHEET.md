# PySpark Cheatsheet

## 1. SparkSession

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ProyectoVentas") \
    .master("local[*]") \
    .getOrCreate()

print(spark.version)
```
# PySpark — Carga de datos: Excel → CSV → PySpark

## 1. Estructura del proyecto

Nuestra estructura:

```text
data_engineering/
│
├── data/
│   ├── clientes.csv
│   ├── productos.csv
│   ├── ventas.csv
│   ├── retail.xlsx
│   ├── retail.csv
│   └── convertir.py
│
└── notebooks/
    └── proyecto.ipynb
```

### ¿Para qué sirve cada carpeta?

* `data/` → guardamos los archivos de datos.
* `notebooks/` → guardamos los notebooks donde trabajamos con PySpark.
* `convertir.py` → script de Python que utilizamos para convertir Excel a CSV.
* `proyecto.ipynb` → notebook donde trabajamos con PySpark.

---

# 2. Excel → CSV con Python y Pandas

Como PySpark trabaja muy bien con CSV, primero convertimos nuestro Excel.

Archivo:

```text
data/convertir.py
```

Código:

```python
import pandas as pd

df = pd.read_excel("data/retail.xlsx")

print(df.head())
print(df.shape)

df.to_csv("data/retail.csv", index=False)

print("CSV creado correctamente")
```

---

## `import pandas as pd`

```python
import pandas as pd
```

### ¿Por qué?

Importamos **Pandas**, una librería de Python que permite trabajar fácilmente con datos y archivos como Excel y CSV.

`pd` es simplemente el nombre abreviado que utilizamos para Pandas.

---

## Leer el Excel

```python
df = pd.read_excel("data/retail.xlsx")
```

### ¿Por qué?

Lee:

```text
data/retail.xlsx
```

y lo convierte en un **DataFrame de Pandas**.

El DataFrame es una estructura parecida a una tabla.

---

## Comprobar las primeras filas

```python
print(df.head())
```

### ¿Por qué?

Nos permite comprobar que Python ha leído correctamente el Excel.

`head()` muestra las primeras 5 filas por defecto.

---

## Comprobar tamaño

```python
print(df.shape)
```

### ¿Por qué?

Nos dice:

```text
(filas, columnas)
```

Por ejemplo:

```text
(500000, 8)
```

significa:

* 500.000 filas
* 8 columnas

---

## Convertir a CSV

```python
df.to_csv("data/retail.csv", index=False)
```

### ¿Por qué?

Guarda nuestro DataFrame como:

```text
data/retail.csv
```

### ¿Qué hace `index=False`?

Evita que Pandas añada una columna extra con:

```text
0
1
2
3
4
...
```

Es decir, no guardamos el índice de Pandas como una columna del CSV.

---

## Confirmar que se ha creado

```python
print("CSV creado correctamente")
```

### ¿Por qué?

Simplemente nos muestra un mensaje para saber que el programa ha terminado.

---

# 3. Ejecutar el script Python

Desde la terminal, estando en la carpeta principal:

```text
/Users/mustafa/data_engineering
```

ejecutamos:

```bash
python data/convertir.py
```

### ¿Qué significa?

Le estamos diciendo a Python:

> Ejecuta el archivo `convertir.py` que está dentro de la carpeta `data`.

Después de ejecutarlo tendremos:

```text
data/
├── retail.xlsx
└── retail.csv
```

---

# 4. Crear el notebook de PySpark

Dentro de:

```text
notebooks/
```

creamos:

```text
proyecto.ipynb
```

### ¿Por qué?

El notebook será nuestro espacio de trabajo para utilizar PySpark.

---

# 5. Importar SparkSession

En `proyecto.ipynb`:

```python
from pyspark.sql import SparkSession
```

### ¿Por qué?

`SparkSession` es el punto de entrada principal para trabajar con PySpark.

Necesitamos una SparkSession para poder crear y trabajar con DataFrames de Spark.

---

# 6. Crear la SparkSession

```python
spark = SparkSession.builder \
    .appName("ProyectoRetail") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()
```

---

## `SparkSession.builder`

```python
SparkSession.builder
```

### ¿Por qué?

Inicia la construcción de nuestra SparkSession.

---

## `.appName()`

```python
.appName("ProyectoRetail")
```

### ¿Por qué?

Le ponemos un nombre a nuestra aplicación Spark.

En nuestro caso:

```text
ProyectoRetail
```

Es principalmente un nombre identificativo.

---

## `.master("local[*]")`

```python
.master("local[*]")
```

### ¿Por qué?

Le indicamos a Spark dónde ejecutarse.

```text
local
```

significa que Spark se ejecutará en nuestro propio ordenador.

```text
*
```

significa que puede utilizar todos los núcleos disponibles.

Esto es especialmente útil cuando estamos practicando PySpark en nuestro Mac.

---

## `.config()`

```python
.config("spark.driver.host", "127.0.0.1")
.config("spark.driver.bindAddress", "127.0.0.1")
```

### ¿Por qué?

Configuramos el driver de Spark para trabajar correctamente en nuestro entorno local.

Estas configuraciones nos ayudaron a evitar problemas de conexión del driver cuando ejecutamos Spark en nuestro Mac.

---

## `.getOrCreate()`

```python
.getOrCreate()
```

### ¿Por qué?

Le dice a Spark:

> Si ya existe una SparkSession, reutilízala. Si no existe, créala.

---

# 7. Leer el CSV con PySpark

```python
retail = spark.read.csv(
    "../data/retail.csv",
    header=True,
    inferSchema=True
)
```

### ¿Qué estamos haciendo?

Estamos leyendo:

```text
retail.csv
```

y creando un DataFrame de PySpark llamado:

```text
retail
```

---

# 8. Entender la ruta `../data/retail.csv`

Nuestro notebook está aquí:

```text
data_engineering/
│
├── data/
│   └── retail.csv
│
└── notebooks/
    └── proyecto.ipynb
```

Estamos trabajando desde `notebooks`.

Para subir desde:

```text
notebooks/
```

a:

```text
data_engineering/
```

utilizamos:

```text
..
```

Por eso:

```python
"../data/retail.csv"
```

significa:

> Sube una carpeta y después entra en `data`.

---

# 9. `header=True`

```python
header=True
```

### ¿Por qué?

Le indica a Spark que **la primera fila del CSV contiene los nombres de las columnas**.

Por ejemplo:

```text
InvoiceNo,StockCode,Description,Quantity,...
```

Spark utilizará esos nombres.

Sin `header=True`, Spark podría tratar esa primera fila como un registro de datos.

---

# 10. `inferSchema=True`

```python
inferSchema=True
```

### ¿Por qué?

Le pedimos a Spark que intente detectar automáticamente el tipo de dato de cada columna.

En nuestro dataset detectó:

```text
InvoiceNo    → string
StockCode    → string
Description  → string
Quantity     → integer
InvoiceDate  → timestamp
UnitPrice    → double
CustomerID   → double
Country      → string
```

Más adelante aprenderemos a definir los tipos manualmente cuando sea necesario.

---

# 11. Mostrar los datos

```python
retail.show()
```

### ¿Por qué?

Muestra las filas del DataFrame.

Por defecto muestra las primeras 20 filas.

Ejemplo:

```text
+---------+---------+--------------------+--------+
|InvoiceNo|StockCode|         Description|Quantity|
+---------+---------+--------------------+--------+
|   536365|   85123A|WHITE HANGING HEA...|       6|
...
```

Sirve para comprobar rápidamente que los datos se han cargado correctamente.

---

# 12. Ver el esquema

```python
retail.printSchema()
```

### ¿Por qué?

Nos muestra la estructura del DataFrame:

* nombre de las columnas
* tipo de dato
* si admite valores nulos

Ejemplo:

```text
root
 |-- InvoiceNo: string
 |-- StockCode: string
 |-- Description: string
 |-- Quantity: integer
 |-- InvoiceDate: timestamp
 |-- UnitPrice: double
 |-- CustomerID: double
 |-- Country: string
```

---

## ⚠️ Importante: los paréntesis `()`

Esto:

```python
retail.printSchema
```

NO ejecuta la función.

Esto:

```python
retail.printSchema()
```

SÍ ejecuta la función.

En Python:

```text
funcion
```

→ referencia a la función

```text
funcion()
```

→ ejecuta la función

---

# 13. Contar las filas

```python
retail.count()
```

### ¿Por qué?

Devuelve el número total de filas del DataFrame.

Es útil para saber cuántos registros tenemos.

---

# 14. Ver los nombres de las columnas

```python
retail.columns
```

### ¿Por qué?

Nos devuelve una lista con los nombres de las columnas.

Por ejemplo:

```python
[
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country"
]
```

---

# 15. Flujo completo que hemos aprendido

```text
        INTERNET
           │
           ▼
     retail.xlsx
           │
           ▼
        data/
           │
           ▼
    Python + Pandas
           │
           ▼
      retail.csv
           │
           ▼
      PySpark
           │
           ▼
    SparkSession
           │
           ▼
    spark.read.csv()
           │
           ▼
    DataFrame retail
           │
           ▼
     show()
     printSchema()
     count()
           │
           ▼
    TRANSFORMACIONES
```

---

# 🧠 CHULETA RÁPIDA

## Excel → CSV

```python
import pandas as pd

df = pd.read_excel("data/retail.xlsx")

df.to_csv("data/retail.csv", index=False)
```

---

## Crear SparkSession

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ProyectoRetail") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()
```

---

## Leer CSV

```python
retail = spark.read.csv(
    "../data/retail.csv",
    header=True,
    inferSchema=True
)
```

---

## Inspeccionar datos

```python
retail.show()
```

```python
retail.printSchema()
```

```python
retail.count()
```

```python
retail.columns
```

---

# Concepto que debemos recordar

Antes de empezar a transformar datos con PySpark, normalmente hacemos:

```text
1. CONSEGUIR LOS DATOS
        ↓
2. GUARDARLOS
        ↓
3. COMPROBARLOS
        ↓
4. CONVERTIRLOS SI ES NECESARIO
        ↓
5. CARGARLOS EN SPARK
        ↓
6. COMPROBAR EL DATAFRAME
        ↓
7. TRANSFORMAR LOS DATOS
```

En nuestro ejercicio:

```text
retail.xlsx
     ↓
Pandas
     ↓
retail.csv
     ↓
PySpark
     ↓
DataFrame retail
     ↓
TRANSFORMACIONES
```



## 2. DataFrames

### Crear

```python
df = spark.createDataFrame(
    [(1, "Ana"), (2, "Juan")],
    ["id", "nombre"]
)
```

### Ver datos

```python
df.show()
```

### Ver estructura

```python
df.printSchema()
```

### Ver columnas

```python
df.columns
```

### Contar filas

```python
df.count()
```

## 3. select()

```python
df.select("nombre", "ciudad").show()
```

### Con F.col()

```python
df.select(
    F.col("nombre"),
    F.col("ciudad")
).show()
```

## 4. F.col()

```python
from pyspark.sql import functions as F

F.col("precio")
```

### Operaciones

```python
F.col("cantidad") * F.col("precio")
```

## 5. withColumn()

```python
ventas_total = ventas.withColumn(
    "total",
    F.col("cantidad") * F.col("precio")
)
```

## 6. when() / otherwise()

```python
ventas = ventas.withColumn(
    "tipo_venta",
    F.when(
        F.col("cantidad") > 1,
        "varias unidades"
    ).otherwise("una unidad")
)
```

### Varias condiciones

```python
F.when(F.col("cantidad") >= 10, "grande") \
 .when(F.col("cantidad") >= 5, "media") \
 .otherwise("pequeña")
```

## 7. filter()

```python
clientes.filter(
    F.col("ciudad") == "Madrid"
).show()
```

### Varias condiciones

```python
df.filter(
    (F.col("precio") > 100) &
    (F.col("cantidad") > 2)
).show()
```

```python
df.filter(
    (F.col("ciudad") == "Madrid") |
    (F.col("ciudad") == "Barcelona")
).show()
```

## 8. isNull() / isNotNull()

```python
df.filter(
    F.col("ciudad").isNull()
).show()
```

```python
df.filter(
    F.col("ciudad").isNotNull()
).show()
```

## 9. fillna()

```python
clientes_limpios = clientes.fillna({
    "ciudad": "desconocida"
})
```

```python
df = df.fillna({
    "ciudad": "desconocida",
    "edad": 0
})
```

## 10. dropna()

```python
df.dropna()
```

```python
df.dropna(
    subset=["ciudad"]
)
```

## 11. drop()

```python
ventas_sin_precio = ventas_total.drop("precio")
```

```python
df.drop("precio", "cantidad")
```

## 12. withColumnRenamed()

```python
ventas_renombrado = ventas_sin_precio.withColumnRenamed(
    "cantidad",
    "unidades"
)
```

## 13. groupBy()

```python
ventas.groupBy("id_cliente")
```

## 14. agg()

```python
total_gastado = ventas_total.groupBy(
    "id_cliente"
).agg(
    F.sum("total").alias("sum_total")
)
```

## 15. Funciones de agregación

```python
F.sum("total")
F.avg("precio")
F.count("id_venta")
F.countDistinct("id_producto")
F.min("precio")
F.max("precio")
```

## 16. alias()

```python
F.sum("total").alias("total_gastado")
```

## 17. countDistinct()

```python
compras_diferentes = ventas.groupBy(
    "id_cliente"
).agg(
    F.countDistinct("id_producto").alias(
        "productos_diferentes"
    )
)
```

## 18. join()

### Inner

```python
ventas_cliente = ventas.join(
    clientes,
    ventas.id_cliente == clientes.id_cliente,
    "inner"
)
```

### Con alias

```python
v = ventas.alias("v")
c = clientes.alias("c")

ventas_cliente = v.join(
    c,
    F.col("v.id_cliente") == F.col("c.id_cliente"),
    "inner"
)
```

### Tipos

```text
inner
left
right
full
```

## 19. orderBy()

### Ascendente

```python
df.orderBy("precio")
```

### Descendente

```python
df.orderBy(
    F.col("precio").desc()
)
```

### Varias columnas

```python
df.orderBy(
    F.col("ciudad").asc(),
    F.col("precio").desc()
)
```

## 20. cast()

```python
df = df.withColumn(
    "id_cliente",
    F.col("id_cliente").cast("string")
)
```

```python
df = df.withColumn(
    "precio",
    F.col("precio").cast("double")
)
```

```python
df = df.withColumn(
    "cantidad",
    F.col("cantidad").cast("long")
)
```

### Tipos importantes

```text
string
int
long
double
float
boolean
date
timestamp
```

## 21. show()

```python
df.show()
```

```python
df.show(20)
```

```python
df.show(truncate=False)
```

## 22. printSchema()

```python
df.printSchema()
```

## 23. Transformations

```text
select()
filter()
withColumn()
drop()
join()
groupBy()
```

## 24. Actions

```text
show()
count()
collect()
```

## 25. F.lit()

```python
df = df.withColumn(
    "pais",
    F.lit("España")
)
```

## 26. Encadenamiento

```python
resultado = df \
    .filter(F.col("precio") > 100) \
    .withColumn(
        "total",
        F.col("cantidad") * F.col("precio")
    ) \
    .select(
        "id_producto",
        "total"
    ) \
    .orderBy(
        F.col("total").desc()
    )

resultado.show()
```

## 27. Ejemplo completo

```python
ventas_total = ventas.withColumn(
    "total",
    F.col("cantidad") * F.col("precio")
)

ventas_tipo = ventas_total.withColumn(
    "tipo_venta",
    F.when(
        F.col("cantidad") > 1,
        "varias unidades"
    ).otherwise("una unidad")
)

total_cliente = ventas_tipo.groupBy(
    "id_cliente"
).agg(
    F.sum("total").alias("total_gastado")
)

resultado = total_cliente.join(
    clientes,
    total_cliente.id_cliente == clientes.id_cliente,
    "inner"
)

resultado.select(
    "id_cliente",
    "nombre",
    "total_gastado"
).orderBy(
    F.col("total_gastado").desc()
).show()
```

## 28. cast()

Cambia el tipo de datos de una columna.

```python
df = df.withColumn(
    "precio",
    F.col("precio").cast("double")
)
```

### Tipos principales

```text
string     → texto
int        → entero
long       → entero grande
bigint     → equivalente a long
float      → decimal
double     → decimal con mayor precisión
boolean    → True / False
date       → fecha
timestamp  → fecha + hora
```

### Ejemplo

```python
ventas = ventas.withColumn(
    "id_cliente",
    F.col("id_cliente").cast("int")
)

ventas = ventas.withColumn(
    "cantidad",
    F.col("cantidad").cast("long")
)

ventas = ventas.withColumn(
    "precio",
    F.col("precio").cast("double")
)
```

Comprobar tipos:

```python
ventas.printSchema()
```

---

## 29. Funciones de texto (Strings)

### lower()

Convierte a minúsculas.

```python
F.lower(F.col("nombre"))
```

Ejemplo:

```python
df = df.withColumn(
    "nombre",
    F.lower(F.col("nombre"))
)
```

### upper()

Convierte a mayúsculas.

```python
F.upper(F.col("nombre"))
```

### trim()

Elimina espacios al principio y al final.

```python
F.trim(F.col("nombre"))
```

### length()

Cuenta caracteres.

```python
F.length(F.col("nombre"))
```

### concat_ws()

Une varias columnas utilizando un separador.

```python
F.concat_ws(
    " ",
    F.col("nombre"),
    F.col("apellido")
)
```

Ejemplo:

```python
df = df.withColumn(
    "nombre_completo",
    F.concat_ws(
        " ",
        F.col("nombre"),
        F.col("apellido")
    )
)
```

### split()

Divide un texto y devuelve un array.

```python
F.split(
    F.col("nombre_completo"),
    " "
)
```

Ejemplo:

```text
"Mostafa Hmidi"
→ ["Mostafa", "Hmidi"]
```

### regexp_replace()

Reemplaza texto.

```python
F.regexp_replace(
    F.col("telefono"),
    "-",
    ""
)
```

Ejemplo:

```text
"600-123-456"
→ "600123456"
```

### Combinar funciones

Las funciones pueden combinarse unas dentro de otras.

Se ejecutan de dentro hacia fuera:

```python
F.lower(
    F.trim(
        F.col("nombre")
    )
)
```

Ejemplo:

```python
df = df.withColumn(
    "nombre_limpio",
    F.lower(
        F.trim(
            F.col("nombre")
        )
    )
)
```

```text
"  MOSTAFA  "
→ "mostafa"
```

### Ejemplo completo

```python
df = df.withColumn(
    "nombre_limpio",
    F.lower(
        F.trim(
            F.col("nombre")
        )
    )
)

df = df.withColumn(
    "nombre_completo",
    F.concat_ws(
        " ",
        F.col("nombre"),
        F.col("apellido")
    )
)

df = df.withColumn(
    "telefono_limpio",
    F.regexp_replace(
        F.col("telefono"),
        "-",
        ""
    )
)
```
# 30. Fechas

```python
from pyspark.sql import functions as F
```

## `to_date()`

Convierte una columna a tipo `date`.

```python
df = df.withColumn(
    "fecha",
    F.to_date(F.col("fecha"))
)
```

Si viene con formato concreto:

```python
df = df.withColumn(
    "fecha",
    F.to_date(F.col("fecha"), "dd/MM/yyyy")
)
```

---

## `year()`

Obtiene el año.

```python
F.year(F.col("fecha"))
```

Ejemplo:

```python
df = df.withColumn(
    "año",
    F.year(F.col("fecha"))
)
```

---

## `month()`

Obtiene el mes.

```python
F.month(F.col("fecha"))
```

---

## `dayofmonth()`

Obtiene el día del mes.

```python
F.dayofmonth(F.col("fecha"))
```

---

## `dayofweek()`

Obtiene el día de la semana.

```python
F.dayofweek(F.col("fecha"))
```

---

## `datediff()`

Calcula la diferencia entre dos fechas en días.

```python
F.datediff(
    F.col("fecha_fin"),
    F.col("fecha_inicio")
)
```

Ejemplo:

```python
df = df.withColumn(
    "dias",
    F.datediff(
        F.col("fecha_fin"),
        F.col("fecha_inicio")
    )
)
```

---

## `date_add()`

Añade días a una fecha.

```python
F.date_add(
    F.col("fecha"),
    7
)
```

→ Añade 7 días.

---

## `date_sub()`

Resta días a una fecha.

```python
F.date_sub(
    F.col("fecha"),
    7
)
```

→ Resta 7 días.

---

## `date_format()`

Cambia el formato de visualización de una fecha.

```python
F.date_format(
    F.col("fecha"),
    "dd/MM/yyyy"
)
```

Ejemplo:

```python
df = df.withColumn(
    "fecha_formateada",
    F.date_format(
        F.col("fecha"),
        "dd/MM/yyyy"
    )
)
```

---

## `current_date()`

Obtiene la fecha actual.

```python
F.current_date()
```

---

## `current_timestamp()`

Obtiene fecha y hora actuales.

```python
F.current_timestamp()
```

---

## Ejemplo completo

```python
df = df.withColumn(
    "fecha",
    F.to_date(
        F.col("fecha"),
        "dd/MM/yyyy"
    )
)

df = df.withColumn(
    "año",
    F.year(F.col("fecha"))
)

df = df.withColumn(
    "mes",
    F.month(F.col("fecha"))
)

df = df.withColumn(
    "dias_desde_inicio",
    F.datediff(
        F.current_date(),
        F.col("fecha")
    )
)
```
## PIVOT

`pivot()` convierte los valores de una columna en nuevas columnas.

Se utiliza después de `groupBy()` y normalmente junto con una agregación.

```python
df.groupBy("Country").pivot("Month").agg(
    F.sum("TotalRevenue")
)
```

Ejemplo:

```text
Country | Month | Revenue
Spain   | 1     | 1000
Spain   | 2     | 1500
France  | 1     | 800
France  | 2     | 900
```

Con `pivot()`:

```text
Country | 1    | 2
Spain   | 1000 | 1500
France  | 800  | 900
```

**Regla mental:**

```text
groupBy → qué quiero en filas
pivot   → qué quiero convertir en columnas
agg     → qué cálculo hago
```

---

## UNION

`union()` sirve para **apilar filas** de dos DataFrames.

```python
df_final = df1.union(df2)
```

Los DataFrames deben tener columnas compatibles y el **orden de las columnas importa**.

```text
df1
Spain
France

+

df2
Germany
Italy

↓

df_final
Spain
France
Germany
Italy
```

### UNIONBYNAME

`unionByName()` también apila filas, pero coloca los valores según el **nombre de las columnas**, no según su posición.

```python
df_final = df1.unionByName(df2)
```

Es más seguro cuando dos DataFrames tienen las mismas columnas pero están en distinto orden.

**Regla mental:**

```text
join → añade columnas
union → añade filas
```

---

## PARTICIONES

Spark divide los datos en **particiones** para poder procesarlos en paralelo.

Puedes consultar el número de particiones:

```python
df.rdd.getNumPartitions()
```

### repartition()

Cambia el número de particiones **redistribuyendo los datos**.

```python
df2 = df.repartition(4)
```

Puede provocar un **shuffle**, porque Spark tiene que mover datos entre particiones.

### coalesce()

Sirve principalmente para **reducir** el número de particiones.

```python
df2 = df.coalesce(4)
```

Si pasamos de 8 → 4, normalmente es más barato que `repartition(4)` porque intenta evitar un shuffle completo.

**Regla mental:**

```text
repartition → redistribuir
coalesce    → reducir
```

---

## SHUFFLE

Un **shuffle** ocurre cuando Spark necesita mover datos entre particiones para reorganizarlos.

Por ejemplo:

```python
df.groupBy("Country").agg(
    F.sum("Quantity")
)
```

Si los datos de `Spain` están repartidos entre varias particiones, Spark tiene que moverlos para poder agruparlos correctamente.

El shuffle puede ser costoso porque implica:

* mover datos entre particiones
* comunicación entre ejecutores en un cluster
* uso de memoria
* posible escritura y lectura desde disco

Operaciones que pueden provocar shuffle:

```text
groupBy()
join()
distinct()
repartition()
```

**Regla mental:**

```text
Procesar datos donde están → barato
Mover datos entre particiones → shuffle → más costoso
```

---

## CACHE

`cache()` sirve para guardar un DataFrame en memoria cuando sabemos que vamos a utilizarlo varias veces.

```python
ventas = retail.filter(
    F.col("Quantity") > 0
)

ventas.cache()
```

Después podemos reutilizar `ventas`:

```python
ventas.count()

ventas.groupBy("Country").count().show()

ventas.groupBy("CustomerID").count().show()
```

Sin cachear, Spark puede tener que volver a calcular las transformaciones anteriores para diferentes acciones.

### Importante: Spark es Lazy

Esto:

```python
ventas.cache()
```

no ejecuta inmediatamente el DataFrame.

Una acción como:

```python
ventas.count()
```

hace que Spark ejecute el procesamiento y pueda materializar el cache.

Cuando ya no necesitamos los datos:

```python
ventas.unpersist()
```

libera el DataFrame cacheado de la memoria.

**Regla mental:**

```text
cache()     → voy a reutilizar estos datos
unpersist() → ya no los necesito
```
# Optimización y rendimiento en PySpark

## 1. `explain()`

`explain()` permite ver el **plan de ejecución** que Spark utilizará para ejecutar una consulta.

```python
df.explain()
```

Sirve para entender qué operaciones realiza Spark y detectar posibles problemas de rendimiento.

Operaciones que podemos encontrar:

* `FileScan` → lectura de los datos.
* `Filter` → aplicación de filtros.
* `Project` → selección o creación de columnas.
* `HashAggregate` → agregaciones como `sum`, `count`, `avg`, etc.
* `Exchange` → movimiento de datos entre particiones (**shuffle**).
* `TakeOrderedAndProject` → operaciones como `orderBy().limit()`.

Ejemplo:

```text
HashAggregate
    ↓
Exchange
    ↓
HashAggregate
    ↓
Filter
    ↓
FileScan
```

Spark puede hacer una **agregación parcial antes del shuffle** para reducir la cantidad de datos que necesita mover.

---

## 2. Shuffle

Un **shuffle** ocurre cuando Spark necesita mover datos entre particiones para poder realizar una operación.

Por ejemplo:

```python
df.groupBy("CustomerID").agg(
    F.sum("Quantity")
)
```

Para agrupar todos los registros del mismo `CustomerID`, Spark necesita llevar los datos correspondientes a la misma clave a una misma partición.

En el plan podemos ver:

```text
Exchange hashpartitioning(CustomerID, 200)
```

`Exchange` normalmente indica que se está produciendo un shuffle.

### Importante

Un shuffle **no significa que el código esté mal**.

Muchas operaciones necesitan shuffle, por ejemplo:

* `groupBy`
* algunos `join`
* `distinct`
* `repartition`
* algunas funciones de ventana

El objetivo es evitar **shuffles innecesarios** y reducir la cantidad de datos que se mueve.

---

## 3. Broadcast

Si tenemos una tabla pequeña y otra grande, podemos utilizar `broadcast()` para evitar un shuffle grande.

```python
from pyspark.sql.functions import broadcast

resultado = ventas.join(
    broadcast(clientes),
    "CustomerID"
)
```

Spark puede copiar la tabla pequeña a las particiones donde se encuentra la tabla grande.

Esto puede producir un:

```text
BroadcastHashJoin
```

en el plan de ejecución.

### Importante

No debemos utilizar `broadcast()` con tablas enormes.

La idea es:

```text
tabla grande + tabla pequeña
        ↓
     broadcast
        ↓
evitar shuffle innecesario
```

---

## 4. Particiones

Podemos consultar cuántas particiones tiene un DataFrame:

```python
df.rdd.getNumPartitions()
```

### `repartition()`

Cambia el número de particiones redistribuyendo los datos.

```python
df.repartition(10)
```

Normalmente implica un **shuffle**.

También podemos repartir utilizando una columna:

```python
df.repartition("CustomerID")
```

### `coalesce()`

Se utiliza principalmente para **reducir** el número de particiones.

```python
df.coalesce(5)
```

Intenta reducir las particiones evitando un shuffle completo cuando sea posible.

### Diferencia básica

```text
repartition → redistribuye los datos → puede hacer shuffle

coalesce → principalmente reduce particiones → intenta evitar shuffle
```

---

## 5. Cache y Persist

Si vamos a utilizar varias veces el mismo DataFrame, podemos guardarlo en memoria para evitar repetir su cálculo.

### `cache()`

```python
df.cache()
```

### `persist()`

Permite elegir cómo queremos almacenar los datos:

```python
from pyspark import StorageLevel

df.persist(StorageLevel.MEMORY_AND_DISK)
```

### Eliminar de la memoria

```python
df.unpersist()
```

### Importante

`cache()` y `persist()` son **lazy**.

El DataFrame no se guarda realmente hasta que Spark ejecuta una acción.

Ejemplo:

```python
df.cache()

df.show()
```

Después de ejecutar una acción, Spark puede reutilizar los datos almacenados en operaciones posteriores.

---

# 6. Data Skew

**Data Skew** significa que los datos están distribuidos de forma muy desigual entre las particiones.

Ejemplo:

```text
Partición 1 → 10.000 registros
Partición 2 → 12.000 registros
Partición 3 → 11.000 registros
Partición 4 → 10.500 registros
Partición 5 → 8.000.000 registros  ← problema
```

Una tarea puede tardar muchísimo más que las demás porque tiene que procesar muchos más datos.

En Spark UI podemos detectar este problema comparando las tareas.

Indicadores importantes:

* Task Duration
* Shuffle Read
* Shuffle Write
* Input Size

Si la mayoría de tareas tardan poco pero una tarda muchísimo más, puede existir **data skew**.

---

# 7. Salting

**Salting** es una técnica para repartir una clave que tiene demasiados datos.

Por ejemplo, si el cliente `50` tiene una cantidad enorme de registros, podemos añadir un valor aleatorio:

```python
retail_salted = retail.withColumn(
    "salt",
    F.when(
        F.col("CustomerID") == 50,
        F.floor(F.rand() * 5)
    ).otherwise(0)
)
```

Para varios clientes:

```python
retail_salted = retail.withColumn(
    "salt",
    F.when(
        F.col("CustomerID").isin(50, 100, 200),
        F.floor(F.rand() * 5)
    ).otherwise(0)
)
```

Esto crea valores de `salt` entre `0` y `4`.

### Importante

Esto **no significa que creemos 5 particiones por cliente**.

Estamos creando 5 posibles valores de una nueva clave para repartir el trabajo.

Podemos crear una clave combinando el cliente y el salt:

```python
retail_salted = retail_salted.withColumn(
    "SaltedCustomerID",
    F.concat(
        F.col("CustomerID").cast("string"),
        F.lit("_"),
        F.col("salt").cast("string")
    )
)
```

Por ejemplo:

```text
CustomerID    salt    SaltedCustomerID

50            0       50_0
50            1       50_1
50            2       50_2
50            3       50_3
50            4       50_4
```

Después hacemos una agregación parcial:

```python
primera_agg = retail_salted.groupBy(
    "CustomerID",
    "SaltedCustomerID"
).agg(
    F.sum("Quantity").alias("PartialQuantity")
)
```

Y finalmente volvemos a agrupar por el cliente original:

```python
resultado = primera_agg.groupBy(
    "CustomerID"
).agg(
    F.sum("PartialQuantity").alias("TotalQuantity")
)
```

### Patrón del Salting

```text
datos
   ↓
añadir salt
   ↓
groupBy(key + salt)
   ↓
agregación parcial
   ↓
groupBy(key)
   ↓
agregación final
```

En un proyecto real, primero debemos identificar qué claves tienen **data skew** y aplicar salting solamente cuando sea necesario.

---

# 8. AQE — Adaptive Query Execution

**AQE (Adaptive Query Execution)** permite que Spark adapte el plan de ejecución durante la ejecución utilizando información real obtenida de los datos.

En el plan podemos ver:

```text
AdaptiveSparkPlan
```

La idea es:

```text
plan inicial
     ↓
ejecución
     ↓
información real de los datos
     ↓
AQE puede adaptar la ejecución
     ↓
mejor rendimiento
```

AQE puede ayudar, entre otras cosas, con:

* Reducir particiones pequeñas después de un shuffle.
* Cambiar la estrategia de un `join`.
* Utilizar broadcast cuando una tabla resulta ser suficientemente pequeña.
* Mitigar algunos problemas de data skew.

---

# 9. Spark UI

Spark UI permite observar cómo se está ejecutando nuestro programa.

Normalmente podemos acceder a:

```text
http://localhost:4040
```

También podemos consultar la URL desde PySpark:

```python
spark.sparkContext.uiWebUrl
```

En Spark UI podemos encontrar información sobre:

* Jobs
* Stages
* Storage
* Environment
* Executors
* SQL / DataFrame

Para analizar **data skew**, nos interesa especialmente observar las tareas de una Stage y comparar:

```text
Task Duration
Shuffle Read
Shuffle Write
Input Size
```

En **Summary Metrics** aparecen estadísticas agregadas como:

```text
Min
Median
Max
```

Pero para detectar claramente qué tarea concreta es problemática necesitamos observar las **tareas individuales**.

---

# 🧠 Idea general de optimización

Cuando analizamos el rendimiento de PySpark podemos pensar:

```text
1. ¿Qué datos estoy leyendo?
        ↓
2. ¿Estoy filtrando pronto?
        ↓
3. ¿Estoy moviendo muchos datos?
        ↓
4. ¿Tengo un Shuffle?
        ↓
5. ¿Tengo Data Skew?
        ↓
6. ¿Puedo utilizar Broadcast?
        ↓
7. ¿Necesito reparticionar?
        ↓
8. ¿Puedo reutilizar datos con Cache/Persist?
        ↓
9. ¿AQE puede optimizar la ejecución?
        ↓
10. Revisar Spark UI
```
