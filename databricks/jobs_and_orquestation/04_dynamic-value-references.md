
# Dynamic Value References in Lakeflow Jobs

## 1. What are Dynamic Value References?

Dynamic Value References allow tasks to access runtime information from a Lakeflow Job.

Databricks replaces these references with their actual values when the task runs.

They use double curly braces:

`{{ }}`

They are commonly used in task parameters, configurations and other supported fields.

## 2. Common Dynamic References

Examples:

| Reference | Description |
|---|---|
| `{{job.id}}` | Job ID |
| `{{job.run_id}}` | Job run ID |
| `{{job.name}}` | Job name |
| `{{job.start_time.iso_date}}` | Job start date |
| `{{task.name}}` | Current task name |
| `{{task.run_id}}` | Task run ID |

The available references depend on the supported context and field.

## 3. Practical Example

Suppose a Job needs to pass its execution date to a notebook.

We configure a task parameter:

```text
run_date = {{job.start_time.iso_date}}
```

Inside the notebook:

```python
run_date = dbutils.widgets.get("run_date")

print(run_date)
```

The notebook receives the date associated with the Job execution.

## 4. Dynamic References vs Widgets

These concepts have different purposes.

### Dynamic Value References

- Obtain information from the Job runtime context.
- Use the `{{ }}` syntax.
- Databricks resolves the value when the task runs.

### Widgets

- Allow notebooks to receive parameters.
- Are created and retrieved through `dbutils.widgets`.
- Make notebook code reusable.

They can work together.

Example:

```text
Task parameter:
run_date = {{job.start_time.iso_date}}
```

Notebook:

```python
run_date = dbutils.widgets.get("run_date")
```

## 5. Dynamic References vs Task Values

| Feature | Dynamic Value References | Task Values |
|---|---|---|
| Source | Job runtime context | Another task |
| Syntax | `{{ }}` | `dbutils.jobs.taskValues.get()` |
| Purpose | Access runtime metadata | Share generated values |
| Example | Job start date | Number of processed records |

## 6. Key Takeaways

- Dynamic Value References use `{{ }}`.
- They access runtime information.
- Databricks resolves them when the task runs.
- They can be passed to notebooks as parameters.
- They are different from Widgets and Task Values.
