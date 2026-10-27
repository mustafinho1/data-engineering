# COPY INTO — Databricks Data Engineering

## 1. What is COPY INTO?

`COPY INTO` is a SQL command used in Databricks to load files from a supported storage location into a Delta table.

It supports incremental file ingestion and tracks successfully loaded files to avoid processing the same files again by default.

It can be executed manually from a Databricks notebook or SQL editor, or scheduled using Lakeflow Jobs.

**Main use cases:**
- Load CSV, JSON, Parquet and other supported file formats.
- Ingest new files incrementally.
- Load selected files from a storage location.
- Retry ingestion without automatically duplicating previously loaded files.

Official documentation: [COPY INTO SQL reference](https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into)

## 2. Basic syntax

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/Volumes/catalog_name/schema_name/volume_name/source_folder/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true');
```

### Main components

- `COPY INTO`: specifies the target table.
- `FROM`: specifies the source file or directory.
- `FILEFORMAT`: defines the source format.
- `FORMAT_OPTIONS`: passes options to the file reader.

The target is a Delta table. The source must be accessible and the necessary permissions must be configured.

## 3. Source locations

`COPY INTO` can read from supported and accessible storage locations, including Unity Catalog Volumes and supported cloud storage locations.

Example using a Unity Catalog Volume:

```sql
COPY INTO first_catalog.default.retail_copy_test
FROM '/Volumes/first_catalog/default/retail_files/retail.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true');
```

A single command has one `FROM` source location. That location can contain multiple files. If data comes from separate source locations, use separate commands or an ingestion solution that coordinates multiple sources.

## 4. Idempotency and incremental ingestion

By default, `COPY INTO` tracks successfully loaded files and skips them in subsequent runs.

This behavior makes it possible to retry the same command without loading the same tracked files again.

### Important characteristics

- Previously loaded files are normally skipped.
- New files added to the source location can be loaded on a subsequent run.
- Modifying an already loaded file does not automatically cause it to be reloaded.
- Uploading the same data under a different filename can result in duplicate rows.
- Idempotency applies to tracked files; it does not guarantee that different files contain different records.

## 5. The `force` option

The `force` option changes the default file-tracking behavior.

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/path/to/source/'
FILEFORMAT = CSV
COPY_OPTIONS ('force' = 'true');
```

When `force = true`, previously loaded files can be loaded again.

**Important:** this can create duplicate rows because the files are processed again. Use it only when intentionally reprocessing data and when duplicate handling has been considered.

## 6. Selecting files with FILES and PATTERN

`FILES` and `PATTERN` allow you to control which files are selected from the source location.

They cannot be used together in the same `COPY INTO` command.

### FILES

Use `FILES` to specify individual filenames.

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/Volumes/catalog_name/schema_name/my_volume/'
FILEFORMAT = CSV
FILES = ('sales_january.csv', 'sales_february.csv')
FORMAT_OPTIONS ('header' = 'true');
```

This selects the two specified files from the source location. The SQL reference documents a maximum of 1,000 files in the `FILES` list.

### PATTERN

Use `PATTERN` to select files using a glob pattern.

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/Volumes/catalog_name/schema_name/my_volume/'
FILEFORMAT = CSV
PATTERN = '*.csv'
FORMAT_OPTIONS ('header' = 'true');
```

Examples of glob patterns:

- `*.csv`: matches filenames ending in `.csv`.
- `sales_*.csv`: matches filenames beginning with `sales_` and ending in `.csv`.
- `?`: matches one character.
- `*`: matches zero or more characters.

**Important:** `PATTERN` uses glob-style matching, not regular expressions.

Official documentation: [COPY INTO SQL reference](https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into)

## 7. VALIDATE

`VALIDATE` checks whether data can be parsed and whether schema, nullability and check constraints are satisfied, without writing the data to the target table.

Example:

```sql
COPY INTO catalog_name.schema_name.target_table
FROM '/path/to/source/'
FILEFORMAT = CSV
VALIDATE ALL
FORMAT_OPTIONS ('header' = 'true');
```

The validation scope can also be limited using `VALIDATE n ROWS`, where supported.

**Main purpose:** identify potential data-loading problems before performing the ingestion.

Check the current SQL reference for the exact syntax and supported validation behavior in your Databricks environment.

## 8. Schema inference and schema evolution

### Schema inference