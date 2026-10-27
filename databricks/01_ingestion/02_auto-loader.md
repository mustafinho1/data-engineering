# Auto Loader in Databricks

## 1. What is Auto Loader?

Auto Loader is a Databricks feature for incrementally and efficiently ingesting new files from cloud object storage into Delta tables.

It uses Apache Spark Structured Streaming through the `cloudFiles` source.

It can process existing files and automatically discover new files as they arrive.

**Main use case:** building scalable ingestion pipelines for files that continuously arrive in cloud storage.

Official documentation: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader

## 2. Why use Auto Loader?

Auto Loader provides:

- **Incremental ingestion:** processes newly discovered files instead of repeatedly loading the entire dataset.
- **Scalability:** designed to handle very large numbers of files.
- **Fault tolerance:** uses a checkpoint to track progress and resume after failures.
- **Schema inference:** can infer the structure of incoming data.
- **Schema evolution:** can be configured to handle new columns.
- **Multiple formats:** supports CSV, JSON, XML, Parquet, Avro, ORC, text, and binary files, subject to format-specific capabilities.

Auto Loader can ingest data from supported cloud storage services and Unity Catalog Volumes.

## 3. How does Auto Loader work?

The ingestion flow is:

1. Files arrive in a source directory.
2. Auto Loader discovers new files.
3. Spark reads and processes the files.
4. Data is written to a Delta table.
5. A checkpoint records ingestion progress.
6. When the pipeline runs again, Auto Loader resumes from its recorded state.

Two important locations:

- **Schema location:** stores schema information used for inference and evolution.
- **Checkpoint location:** stores streaming progress and state.

These locations serve different purposes. Keep them separate from the source files, and use a persistent checkpoint for each independent ingestion workload.

## 4. Basic PySpark example

This example ingests CSV files from a Unity Catalog Volume into a Delta table.

```python
source_path = "/Volumes/catalog_name/schema_name/volume_name/incoming/"

schema_path = "/Volumes/catalog_name/schema_name/volume_name/metadata/schemas/retail"

checkpoint_path = "/Volumes/catalog_name/schema_name/volume_name/metadata/checkpoints/retail"

target_table = "catalog_name.schema_name.retail_autoloaded"
```

Configure Auto Loader:

```python
df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("header", "true")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaLocation", schema_path)
    .load(source_path)
)
```

Write the data into a Delta table:

```python
query = (
    df.writeStream
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable(target_table)
)
```

### What does each part do?

- `readStream`: creates a streaming DataFrame.
- `format("cloudFiles")`: activates Auto Loader.
- `cloudFiles.format`: specifies the source file format.
- `header`: tells the CSV reader that the first row contains column names.
- `cloudFiles.inferColumnTypes`: enables column type inference for supported formats such as CSV.
- `cloudFiles.schemaLocation`: stores schema information.
- `writeStream`: defines the streaming output.
- `checkpointLocation`: tracks processing progress.
- `trigger(availableNow=True)`: processes the files available for that run, potentially across multiple micro-batches, and then stops.
- `toTable`: writes the stream to a table.

**Important:** Replace the example paths and table name with your actual catalog, schema, Volume paths, and target table. Keep the source directory separate from the metadata directories.

## 5. Continuous streaming vs. AvailableNow

Auto Loader can be used in different execution patterns.

### Continuous processing

```python
query = (
    df.writeStream
    .option("checkpointLocation", checkpoint_path)
    .toTable(target_table)
)
```

This runs continuously until stopped or until the query fails. It is useful when low-latency ingestion is required.

### AvailableNow

```python
query = (
    df.writeStream
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable(target_table)
)
```

This processes the files available when the run starts and then terminates. It can be scheduled with Lakeflow Jobs.

**Use AvailableNow when:** files arrive periodically, such as once per hour or once per day, and you don't need a continuously running stream.

## 6. Schema inference and schema evolution

Auto Loader can infer the schema of incoming files and can be configured to handle changes.

For example, suppose the original CSV contains:

```text
customer_id,name
1,Alice
2,Bob
```

Later files contain an additional column:

```text
customer_id,name,country
3,Charlie,Spain
```

Auto Loader's behavior depends on the configured schema evolution mode.

| Mode | Behavior |
|---|---|
| `addNewColumns` | Detects new columns and updates the inferred schema; the stream fails and must restart to continue with the updated schema. |
| `rescue` | Does not evolve the schema; unexpected fields are captured in the rescued data column when configured. |
| `failOnNewColumns` | Fails when new columns are detected and requires intervention. |
| `none` | Does not evolve the schema; new columns are ignored unless rescued data is configured. |

The default depends on whether you provide a schema. Without a provided schema, `addNewColumns` is the default; with a provided schema, `none` is the default.

Schema evolution in Auto Loader and schema evolution in the destination Delta table are separate concerns. The destination table must also be able to accept the changed schema.

Official documentation: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema

## 7. Checkpoints and exactly-once processing

Auto Loader uses its checkpoint to track discovered and processed files.

With a persistent checkpoint and a supported Delta Lake sink, it provides exactly-once processing semantics for the ingestion pipeline under the documented conditions.

Important rules:

- Do not delete the checkpoint casually.
- Reuse the same checkpoint when restarting the same pipeline.
- Use a different checkpoint for an independent pipeline.
- Do not assume that deleting the checkpoint is a harmless reset; files may be processed again.
- By default, Auto Loader expects files to be immutable. If files are overwritten, reprocessing behavior requires additional configuration and duplicate handling.

A checkpoint helps prevent accidental reprocessing; it does not replace data-quality checks or business-level deduplication.

FAQ: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/faq

## 8. Auto Loader vs. COPY INTO

| Feature | Auto Loader | COPY INTO |
|---|---|---|
| Main purpose | Scalable incremental ingestion | Incremental file loading using SQL |
| Interface | Structured Streaming with `cloudFiles`; also available through managed pipeline and SQL experiences | SQL command |
| File discovery | Designed for efficient discovery at large scale | Tracks files loaded by the command |
| Schema inference and evolution | Built-in configurable capabilities | Different schema-handling workflow |
| Operational state | Uses a streaming checkpoint | Maintains ingestion state for incremental loading |
| Best fit | Large or growing file collections and recurring ingestion | Simpler SQL-driven loads and selected file reprocessing |

Neither tool is universally better. Choose based on the volume of files, schema changes, operational requirements, and how much control the pipeline needs.

Official comparison: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage

## 9. Common mistakes

- Putting the checkpoint inside a directory being ingested as source data.
- Reusing one checkpoint for unrelated streams.
- Deleting a checkpoint and expecting the pipeline to resume exactly where it stopped.
- Assuming schema inference automatically makes the target Delta table evolve.
- Assuming `availableNow=True` means continuous streaming.
- Expecting Auto Loader to process overwritten files again while `cloudFiles.allowOverwrites` remains at its default value of `false`.
- Using an empty source directory without providing a schema; inference requires data to inspect.

## 10. When should you use Auto Loader?

Choose Auto Loader when you need to ingest files incrementally, especially when the number of files is large or the schema may change over time.

For production workloads, consider running it through Lakeflow Jobs or Lakeflow pipelines, with durable checkpoints, monitoring, permissions, and data-quality controls.

Best practices: https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/best-practices
