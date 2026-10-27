# Semi-Structured JSON Ingestion with PySpark

## 1. CSV vs JSON

CSV and JSON are common source formats in data engineering. The main difference is how they represent data.

| Feature | CSV | JSON |
|---|---|---|
| Structure | Rows and columns | Objects, arrays, and nested structures |
| Schema | Often requires explicit types or schema inference | Spark can infer the schema when reading |
| Nested data | No native nested structure | Supports nested objects and arrays |
| Common sources | Excel exports, sales reports, database extracts | APIs, application events, logs |
| Common challenges | Delimiters, quoting, inconsistent types | Schema changes, missing fields, malformed records |

### Reading CSV

```python
df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(path)
)
```

- `header=True`: uses the first row as column names.
- `inferSchema=True`: asks Spark to infer column types. This may require additional work during reading.

### Reading JSON

```python
df = spark.read.json(path)
```

Spark infers the schema by examining the JSON records. For production pipelines, an explicit schema can provide more predictable data types and behavior.

### Inspecting the data

```python
df.printSchema()
df.show(truncate=False)
```

Inspect both the schema and sample values before deciding which transformations are necessary.

---

## 2. Understanding Nested JSON Structures

JSON can contain objects and collections inside other objects.

### STRUCT

A `STRUCT` represents an object with named fields.

Example:

```json
{
  "customer_id": 101,
  "name": "Ali",
  "address": {
    "city": "Madrid",
    "country": "Spain"
  }
}
```

Access nested fields using dot notation:

```python
df.select(
    "customer_id",
    "name",
    "address.city"
)
```

You can rename the extracted field:

```python
from pyspark.sql import functions as F

df.select(
    "customer_id",
    F.col("address.city").alias("city")
)
```

### ARRAY

An `ARRAY` represents a collection of elements, such as a list of orders.

```json
{
  "customer_id": 101,
  "orders": [
    {"order_id": 1, "amount": 50},
    {"order_id": 2, "amount": 80}
  ]
}
```

Use `explode()` when each element needs to become a separate row.

```python
df_exploded = df.withColumn(
    "order",
    F.explode("orders")
)

df_orders = df_exploded.select(
    "customer_id",
    F.col("order.order_id").alias("order_id"),
    F.col("order.amount").alias("amount")
)
```

Result:

| customer_id | order_id | amount |
|---:|---:|---:|
| 101 | 1 | 50 |
| 101 | 2 | 80 |

**Important:** `explode()` normally produces one row per array element. An empty or null array produces no rows with ordinary `explode()`. Use `explode_outer()` when you need to preserve the parent row in those cases.

### MAP

A `MAP` represents key-value pairs.

For example, a map could contain a customer's preferences:

```json
{
  "customer_id": 101,
  "preferences": {
    "language": "en",
    "theme": "dark"
  }
}
```

If `preferences` is represented as a Spark map, access a key with:

```python
df.select(
    "customer_id",
    F.col("preferences")["language"].alias("language")
)
```

The exact access pattern depends on whether the field is represented as a `MAP` or a `STRUCT`. Check `printSchema()` first.

---

## 3. `from_json()`

`from_json()` parses a column containing JSON text and converts it into a typed Spark structure.

### When to use it

Use `from_json()` when a column is a `STRING` containing JSON text.

Example source data:

| customer_id | details |
|---:|---|
| 101 | `{"city":"Madrid","age":30}` |
| 102 | `{"city":"Sevilla","age":25}` |

The `details` column contains JSON text rather than an already parsed structure.

### Define the schema and parse the column

```python
from pyspark.sql import functions as F

schema = "city STRING, age INT"

df_parsed = df.withColumn(
    "details_parsed",
    F.from_json(F.col("details"), schema)
)
```

Inspect the result:

```python
df_parsed.printSchema()
```

The new `details_parsed` column is a `STRUCT` with `city` and `age` fields.

Extract the fields:

```python
df_result = df_parsed.select(
    "customer_id",
    F.col("details_parsed.city").alias("city"),
    F.col("details_parsed.age").alias("age")
)
```

### `spark.read.json()` vs `from_json()`

| Function | Purpose |
|---|---|
| `spark.read.json(path)` | Reads JSON files into a DataFrame |
| `F.from_json(column, schema)` | Parses JSON text stored inside a DataFrame column |

**Rule:** Read JSON files with `spark.read.json()`. Parse JSON text inside a column with `from_json()`.

`from_json()` requires a schema. Malformed or incompatible values may result in nulls or other parsing behavior depending on the data, schema, and parsing options.

---

## 4. Explicit Schemas vs Schema Inference

Spark can infer a schema, but inference does not guarantee that every record is valid or that the schema will remain stable.

### Define an explicit schema

```python
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType
)

schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

df = spark.read.schema(schema).json(path)
```

Advantages:

- Controls expected data types.
- Makes the pipeline's expectations explicit.
- Helps maintain consistency between runs.
- Avoids relying entirely on inferred types.

An explicit schema does not automatically validate all business rules or guarantee that all records are valid. Data-quality checks are still necessary.

---

## 5. Missing Fields, Incompatible Types, and Malformed JSON

These are different data-quality problems and should not be treated as identical.

### Missing fields

Example:

```json
{"customer_id": 102, "name": "Sara"}
```

If `age` is part of the schema but absent from this record, the resulting `age` value will normally be `null`.

### Incompatible types

Example:

```json
{"customer_id": 103, "name": "Omar", "age": "unknown"}
```

If the schema expects `age INT`, the value `"unknown"` cannot be represented as a valid integer. Parsing can produce a null value for the incompatible field.

### Malformed JSON

Example:

```json
{"customer_id": 104, "name": "Omar"
```

The object is incomplete because it lacks a closing brace. This is a parsing problem, not simply a missing field.

### Production considerations

A robust pipeline should decide how to handle:

- Missing required fields.
- Invalid or incompatible values.
- Malformed JSON records.
- Records that fail business rules.

Depending on the requirements, invalid records may be logged, quarantined, rescued where supported, or rejected. Do not assume Spark automatically repairs malformed JSON or removes every invalid record.

---

## 6. Auto Loader and Schema Evolution

Auto Loader incrementally ingests new files from cloud storage into Databricks.

It supports formats including CSV and JSON. Schema handling is especially important when incoming files change over time.

### Schema evolution modes

| Mode | General behavior |
|---|---|
| `addNewColumns` | Detects new columns, updates the stored schema, and normally stops the stream with an exception so it can restart with the updated schema |
| `rescue` | Does not evolve the schema for new fields; unexpected data can be retained in `_rescued_data` |
| `failOnNewColumns` | Stops the stream when new columns are detected |
| `none` | Does not evolve the schema and does not automatically rescue unexpected columns |

The exact behavior depends on the source format and configuration. In particular, the `rescue` mode requires the rescued-data column to be configured appropriately.

### Example: New field appears

Initial JSON:

```json
{"customer_id": 101, "name": "Ali"}
```

Later JSON:

```json
{"customer_id": 102, "name": "Sara", "email": "sara@example.com"}
```

The pipeline must have a defined strategy for the new `email` field.

With `addNewColumns`, Auto Loader can detect the new field, update the schema, and stop the stream. The stream can then be restarted to continue with the updated schema.

With `rescue`, unexpected fields can be retained in `_rescued_data` for later inspection rather than automatically becoming regular columns.

### Example configuration

```python
df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", schema_location)
    .option("cloudFiles.schemaEvolutionMode", "rescue")
    .load(source_path)
)
```

This example assumes `source_path` and `schema_location` are defined. Configure the rescued-data column and checkpoint location appropriately for the complete streaming pipeline.

**Important:** Schema evolution and malformed-record handling solve different problems. A new field may be valid JSON but unexpected under the current schema; malformed JSON may not be parseable at all.

---

## 7. Recommended Data Engineering Workflow

A practical workflow for semi-structured JSON data is:

1. Identify the source format and inspect sample records.
2. Read the data with the appropriate Spark reader.
3. Inspect the schema using `printSchema()`.
4. Decide whether schema inference or an explicit schema is appropriate.
5. Parse JSON strings with `from_json()` when needed.
6. Extract nested fields and flatten arrays with `explode()` when required.
7. Validate missing fields, incompatible types, and malformed records.
8. Define how schema changes will be handled.
9. Apply business transformations and data-quality rules.
10. Write the validated result to a suitable destination, such as Delta tables.

### Example workflow

```python
from pyspark.sql import functions as F

# 1. Read JSON files
df = spark.read.json(path)

# 2. Inspect the schema and sample data
df.printSchema()
df.show(truncate=False)

# 3. Extract nested fields
df_customers = df.select(
    "customer_id",
    "name",
    F.col("address.city").alias("city")
)

# 4. Validate required fields
df_valid_customers = df_customers.filter(
    F.col("customer_id").isNotNull()
)

# 5. Continue with the required business transformations
```

This is an illustrative workflow. The actual transformations and validation rules depend on the source schema and business requirements.

---

## 8. Key Takeaways

- CSV is naturally tabular; JSON can contain nested objects and arrays.
- `printSchema()` helps identify the structure and types of the data.
- `STRUCT` represents an object, `ARRAY` represents a collection, and `MAP` represents key-value pairs.
- Use `explode()` to create rows from array elements.
- Use `from_json()` to parse JSON text stored in a column.
- Explicit schemas provide control, but they do not replace data-quality validation.
- Missing fields, incompatible values, and malformed JSON are different problems.
- Auto Loader supports incremental ingestion and schema evolution for CSV and JSON.
- `addNewColumns` and `rescue` have different behaviors; choose based on the pipeline's requirements.
- Once the data is structured, most business transformations use the same PySpark operations regardless of whether the original source was CSV or JSON.

## Official Documentation

- [Read JSON files — Databricks](https://docs.databricks.com/aws/en/query/formats/json)
- [Auto Loader schema inference and evolution](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema)
- [Semi-structured data — Databricks](https://docs.databricks.com/aws/en/semi-structured/)
