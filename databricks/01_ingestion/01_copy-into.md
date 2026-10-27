# 1. COPY INTO

## 1.1. What is COPY INTO?

`COPY INTO` is a Databricks SQL command used to incrementally load files from a supported storage location into a Delta table.

It tracks successfully loaded files and skips them on subsequent runs by default.

**Main use cases:**
- Incremental batch ingestion from files.
- Loading selected files from a storage location.
- Retrying ingestion without reloading previously processed files.
- Loading data from formats such as CSV, JSON and Parquet, where supported.

Official documentation: [COPY INTO — SQL reference](https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into)

## 1.2. Basic syntax

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/Volumes/catalog_name/schema_name/volume_name/source_folder/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true');
```

### Main components

- `COPY INTO`: identifies the target table.
- `FROM`: specifies the source location.
- `FILEFORMAT`: declares the source file format.
- `FORMAT_OPTIONS`: configures how the source files are read.

The target is a Delta table. The source location must be accessible and the necessary permissions must be configured.

## 1.3. Execution and automation

`COPY INTO` can be executed manually from a Databricks notebook or SQL editor.

It can also be scheduled or orchestrated using Lakeflow Jobs.

**Important distinction:**
- `COPY INTO` performs the file ingestion.
- Lakeflow Jobs schedules and orchestrates tasks.

## 1.4. Source locations

`COPY INTO` can read from supported and accessible storage locations, including Unity Catalog Volumes and supported cloud storage locations.

A single command has one `FROM` source location, but that location can contain multiple files.

For separate source locations, use separate commands or an ingestion solution that coordinates multiple sources.

Example:

```sql
COPY INTO first_catalog.default.retail_copy_test
FROM '/Volumes/first_catalog/default/retail_files/retail.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true');
```

## 1.5. Idempotency and incremental ingestion

By default, `COPY INTO` tracks successfully loaded files and skips them on subsequent runs.

This behavior makes retries safer because the same tracked files are not normally loaded again.

**Important characteristics:**
- Previously loaded files are normally skipped.
- New files added to the source location can be loaded on a subsequent run.
- Modifying an already loaded file does not automatically cause it to be reloaded.
- Uploading the same data under a different filename can lead to duplicate rows.
- File-level tracking does not guarantee that different files contain different records.

## 1.6. The `force` option

The `force` option changes the default file-tracking behavior.

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/path/to/source/'
FILEFORMAT = CSV
COPY_OPTIONS ('force' = 'true');
```

When `force = true`, previously loaded files can be loaded again.

**Warning:** this can create duplicate rows. Use it only when intentionally reprocessing files and when duplicate handling has been considered.

## 1.7. Selecting files with FILES and PATTERN

`FILES` and `PATTERN` control which files are selected from the source location. They cannot be used together in the same command.

### FILES

Use `FILES` to specify individual filenames.

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/Volumes/catalog_name/schema_name/my_volume/'
FILEFORMAT = CSV
FILES = ('sales_january.csv', 'sales_february.csv')
FORMAT_OPTIONS ('header' = 'true');
```

The `FILES` list supports up to 1,000 files.

### PATTERN

Use `PATTERN` to select filenames using a glob pattern.

```sql
COPY INTO catalog_name.schema_name/target_table
FROM '/Volumes/catalog_name/schema_name/my_volume/'
FILEFORMAT = CSV
PATTERN = '*.csv'
FORMAT_OPTIONS ('header' = 'true');
```

Examples:
- `*.csv`: matches filenames ending in `.csv`.
- `sales_*.csv`: matches filenames beginning with `sales_` and ending in `.csv`.
- `*`: matches zero or more characters.
- `?`: matches one character.

**Exam note:** `PATTERN` uses glob-style matching, not regular expressions.

## 1.8. VALIDATE

`VALIDATE` checks whether source data can be parsed and whether applicable schema, nullability and check constraints are satisfied, without writing the data to the target table.

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/path/to/source/'
FILEFORMAT = CSV
VALIDATE ALL
FORMAT_OPTIONS ('header' = 'true');
```

Where supported, validation can also be limited using `VALIDATE n ROWS`.

**Main purpose:** identify potential data-loading problems before ingestion.

Check the current SQL reference for exact syntax and supported validation behavior.

## 1.9. Schema inference and evolution

- **Schema inference** attempts to determine source column types.
- **Schema evolution** allows the target schema to adapt to compatible incoming changes.

For example, `COPY_OPTIONS ('mergeSchema' = 'true')` can enable schema evolution where supported.

These concepts are different. Schema inference determines source types; schema evolution changes the target schema.

A source and target column can have the same name but incompatible data types. For example, `Quantity` might be inferred as `STRING` while the target defines it as `INT`.

When an error such as `Failed to merge quantity and quantity` occurs, inspect the source schema, target schema and reader options.

## 1.10. Corrupt files

In supported environments, reader options such as `ignoreCorruptFiles` can allow corrupt files to be skipped.

Important considerations:
- Skipping a corrupt file does not mean its data was successfully ingested.
- A skipped file may be processed on a later run after the underlying issue is fixed.
- Inspect the command result and metrics to understand what was loaded or skipped.

Use `VALIDATE` when appropriate to identify parsing and schema problems before loading.

## 1.11. COPY INTO vs Auto Loader

### COPY INTO

Useful for incremental file ingestion when SQL-based control and explicit file selection are important.

Characteristics:
- SQL-based ingestion.
- Tracks successfully loaded files.
- Supports explicit file selection.
- Can be run manually or orchestrated with jobs.

### Auto Loader

Designed for scalable incremental file ingestion, especially when files arrive continuously or in very large volumes.

It provides capabilities for file discovery, checkpointing and schema inference/evolution.

### General rule of thumb

- Choose `COPY INTO` for straightforward incremental ingestion and explicit control over file selection.
- Consider Auto Loader for large-scale file ingestion, continuous arrivals and more advanced ingestion workflows.

The best choice depends on scale, file-arrival patterns, schema changes and operational requirements.

## 1.12. Practical work completed

Workspace: `first_catalog`

Unity Catalog Volume:

`/Volumes/first_catalog/default/retail_files/`

Source file:

`/Volumes/first_catalog/default/retail_files/retail.csv`

Original Delta table:

`first_catalog.default.retail`

Practice target table:

`first_catalog.default.retail_copy_test`

The CSV was created from `retail.xlsx`, loaded into Databricks and used to practise `COPY INTO`.

The original `retail` table should remain unchanged during ingestion exercises.

## 1.13. Official documentation

- [COPY INTO — SQL reference](https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into)
- [Get started using COPY INTO](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into)
- [Common COPY INTO examples](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into/examples)
- [Cloud object storage ingestion](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage)
