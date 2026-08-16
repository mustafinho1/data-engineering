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
