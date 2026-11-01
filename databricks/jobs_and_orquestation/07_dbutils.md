
# dbutils in Databricks

## 1. What is dbutils?

`dbutils` stands for Databricks Utilities.

It provides utilities that help interact with the Databricks environment from notebooks.

It is not a replacement for PySpark. It complements Spark operations with additional functionality.

## 2. dbutils.fs — File System Utilities

Used to work with files and directories.

Common operations:

```python
# List files and directories
dbutils.fs.ls("/Volumes/first_catalog/default/my_volume/")

# Create a directory
dbutils.fs.mkdirs("/Volumes/first_catalog/default/my_volume/archive/")

# Copy a file
dbutils.fs.cp(
    "/Volumes/first_catalog/default/my_volume/customers.csv",
    "/Volumes/first_catalog/default/my_volume/archive/customers.csv"
)

# Move a file
dbutils.fs.mv(
    "/Volumes/first_catalog/default/my_volume/customers.csv",
    "/Volumes/first_catalog/default/my_volume/archive/customers.csv"
)

# Remove a file
dbutils.fs.rm(
    "/Volumes/first_catalog/default/my_volume/archive/customers.csv"
)
```

Typical use cases:

- Inspect files in a Volume.
- Organize incoming files.
- Move processed files.
- Remove temporary files.

Be careful with destructive operations such as `rm`.

## 3. dbutils.widgets — Notebook Parameters

Widgets allow notebooks to receive parameters.

Create widgets:

```python
dbutils.widgets.text("source_file", "")
dbutils.widgets.text("table_name", "")
```

Retrieve their values:

```python
source_file = dbutils.widgets.get("source_file")
table_name = dbutils.widgets.get("table_name")
```

Typical use cases:

- Reuse one notebook for multiple datasets.
- Pass parameters from Lakeflow Jobs tasks.
- Avoid hardcoding filenames and table names.

In our ingestion project, six tasks can reuse the same notebook with different parameter values.

## 4. dbutils.jobs.taskValues — Share Values Between Tasks

Task Values allow one task to publish a small value that another task can retrieve during the same Job run.

Publish a value:

```python
dbutils.jobs.taskValues.set(
    key="processed_count",
    value=1000
)
```

Retrieve a value:

```python
processed_count = dbutils.jobs.taskValues.get(
    taskKey="Task_A",
    key="processed_count"
)
```

Typical use cases:

- Share row counts.
- Pass execution metadata.
- Communicate simple results between tasks.

Important:

- Task Values are for small values, not DataFrames.
- The publishing task must execute before the consuming task.
- Configure task dependencies when execution order matters.

## 5. dbutils.secrets — Secrets Management

Used to retrieve secrets stored in Databricks secret scopes.

Example:

```python
password = dbutils.secrets.get(
    scope="my_scope",
    key="database_password"
)
```

Typical use cases:

- Database passwords.
- API tokens.
- Credentials for external services.

Important:

- Do not hardcode credentials in notebooks.
- Do not print secrets.
- Access depends on the permissions configured for the secret scope.

## 6. dbutils.notebook — Notebook Execution

Allows one notebook to execute another notebook.

Example:

```python
result = dbutils.notebook.run(
    "/Shared/child_notebook",
    60,
    {"source_file": "customers.csv"}
)
```

The arguments include:

- Notebook path.
- Timeout in seconds.
- Parameters passed to the notebook.

A notebook can return a value using:

```python
dbutils.notebook.exit("SUCCESS")
```

The calling notebook receives the returned value.

Typical use cases:

- Execute reusable notebook logic.
- Organize notebook-based workflows.
- Pass parameters and receive results.

For production orchestration, Lakeflow Jobs provides a more structured way to define tasks and dependencies.

## 7. Other dbutils Modules

Databricks has additional utilities, including:

- `dbutils.library`: library-related functionality in supported environments.
- `dbutils.entry_point`: internal and advanced functionality.

Not every utility is available in every execution environment.

## 8. dbutils Quick Reference

| Module | Main purpose |
|---|---|
| `dbutils.fs` | Work with files and directories |
| `dbutils.widgets` | Create and retrieve notebook parameters |
| `dbutils.jobs.taskValues` | Share small values between Job tasks |
| `dbutils.secrets` | Retrieve stored secrets |
| `dbutils.notebook` | Execute notebooks and return values |
| `dbutils.library` | Library-related operations |

## 9. Key Takeaways

- `dbutils` complements PySpark in Databricks notebooks.
- `fs` works with files and directories.
- `widgets` receive notebook parameters.
- `taskValues` share small values between tasks.
- `secrets` retrieve credentials securely.
- `notebook.run()` executes another notebook.
- `notebook.exit()` returns a value to the calling notebook.
