
# Job Parameters, Task Parameters and Widgets

## 1. Job Parameters

Job Parameters are key-value pairs defined at the Job level.

They allow us to pass shared configuration values to multiple tasks.

Examples:

- environment = production
- catalog = first_catalog
- schema = default

A Job Parameter can be referenced by tasks within the Job.

## 2. Task Parameters

Task Parameters are key-value pairs configured for an individual task.

They allow each task to receive different values.

Example:

| Task | source_file |
|---|---|
| Task 1 | customers.csv |
| Task 2 | products.csv |
| Task 3 | orders.csv |

If a Job Parameter and a Task Parameter use the same key, the Task Parameter takes precedence for that task.

## 3. Notebook Widgets

Widgets allow notebooks to receive and retrieve parameters.

Common widget types:

- text()
- dropdown()
- combobox()
- multiselect()

### Creating a text widget

```python
dbutils.widgets.text("source_file", "")
```

Arguments:

- First argument: parameter name.
- Second argument: default value.

### Retrieving a parameter

```python
source_file = dbutils.widgets.get("source_file")
```

The notebook receives the value configured when the task runs.

## 4. Practical Example: Reusing One Notebook

We can reuse a single notebook to ingest six different CSV files.

### Step 1: Create widgets

```python
dbutils.widgets.text("source_file", "")
dbutils.widgets.text("table_name", "")
dbutils.widgets.text(
    "volume_path",
    "/Volumes/first_catalog/default/my_volume/"
)
```

### Step 2: Retrieve parameters

```python
source_file = dbutils.widgets.get("source_file")
table_name = dbutils.widgets.get("table_name")
volume_path = dbutils.widgets.get("volume_path")
```

### Step 3: Read the CSV

```python
file_path = volume_path + source_file

df = (
    spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(file_path)
)
```

### Step 4: Save as a Delta table

```python
(
    df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        f"first_catalog.default.{table_name}"
    )
)
```

## 5. Job Configuration

The same notebook is configured in six different Tasks.

| Task | source_file | table_name |
|---|---|---|
| Task 1 | customers.csv | customers |
| Task 2 | products.csv | products |
| Task 3 | orders.csv | orders |
| Task 4 | orders_items.csv | orders_items |
| Task 5 | payments.csv | payments |
| Task 6 | refunds.csv | refunds |

Each task passes different parameter values to the same notebook.

## 6. Important Differences

| Feature | Job Parameters | Task Parameters | Widgets |
|---|---|---|---|
| Scope | Job | Individual task | Notebook |
| Purpose | Shared configuration | Task-specific configuration | Create and retrieve notebook inputs |
| Configuration | Job settings | Task settings | Notebook code |

## 7. Key Takeaways

- Job Parameters provide shared configuration.
- Task Parameters provide task-specific values.
- Widgets allow notebooks to retrieve parameters.
- `dbutils.widgets.text()` creates a text widget.
- `dbutils.widgets.get()` retrieves its value.
- Task-level values take precedence over Job-level values when keys overlap.
- One notebook can be reused by multiple tasks with different parameters.
