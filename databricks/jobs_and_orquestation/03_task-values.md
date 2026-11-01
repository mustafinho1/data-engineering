
# Task Values in Lakeflow Jobs

## 1. What are Task Values?

Task Values allow tasks within the same Lakeflow Job to share small pieces of information during execution.

They are useful when one task generates a value that another task needs.

Examples:

- Number of records processed.
- Number of rejected records.
- Name of a generated table.
- Validation results.
- Processing status.

Task Values are not designed to transfer complete DataFrames between tasks.

## 2. Publishing a Task Value

Use:

`dbutils.jobs.taskValues.set()`

Example:

```python
dbutils.jobs.taskValues.set(
    key="processed_count",
    value=1500
)
```

Arguments:

- `key`: name used to identify the value.
- `value`: information to publish.

## 3. Retrieving a Task Value

Use:

`dbutils.jobs.taskValues.get()`

Example:

```python
processed_count = dbutils.jobs.taskValues.get(
    taskKey="Task_A",
    key="processed_count"
)

print(processed_count)
```

Arguments:

- `taskKey`: name of the task that published the value.
- `key`: name of the published value.

## 4. Practical Example

A Job contains two tasks:

### Task A: Data Ingestion

Task A reads a CSV file and counts the processed records.

```python
processed_count = df.count()

dbutils.jobs.taskValues.set(
    key="processed_count",
    value=processed_count
)
```

### Task B: Data Validation

Task B retrieves the number of processed records.

```python
processed_count = dbutils.jobs.taskValues.get(
    taskKey="Task_A",
    key="processed_count"
)

if processed_count == 0:
    raise Exception("No records were processed")
```

Task B can use the value published by Task A to validate the ingestion.

## 5. Task Dependencies

Task Values can be retrieved by other tasks in the same Job.

However, execution order is important.

If Task B needs a value published by Task A, Task B should depend on Task A.

Example:

```text
Task A
  |
  v
Task B
```

This ensures Task A completes before Task B attempts to retrieve its value.

## 6. Task Values vs Widgets

| Feature | Widgets | Task Values |
|---|---|---|
| Purpose | Receive notebook parameters | Share runtime values between tasks |
| Created using | `dbutils.widgets.text()` | `dbutils.jobs.taskValues.set()` |
| Retrieved using | `dbutils.widgets.get()` | `dbutils.jobs.taskValues.get()` |
| Typical use | Select source file | Share processed record count |

## 7. Important Considerations

- Task Values are scoped to a Lakeflow Job run.
- They are intended for small values, not large datasets.
- The publishing task must execute before its value can be retrieved.
- `taskKey` identifies the publishing task.
- Dependencies should guarantee the correct execution order.

## 8. Key Takeaways

- `set()` publishes a Task Value.
- `get()` retrieves a Task Value.
- Task Values allow communication between tasks.
- They are useful for passing metadata and processing results.
- They do not replace DataFrames, Delta tables or data storage.
