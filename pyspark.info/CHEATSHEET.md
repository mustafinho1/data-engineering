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
