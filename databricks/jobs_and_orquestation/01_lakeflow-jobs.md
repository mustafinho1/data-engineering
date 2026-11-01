
# Lakeflow Jobs

## 1. What is Lakeflow Jobs?

Lakeflow Jobs is Databricks' orchestration service. It allows us to automate, schedule, monitor and manage data workflows.

A Job is a collection of tasks that execute according to a defined workflow.

### Main components

- **Job:** The complete workflow.
- **Task:** An individual unit of work within a Job.
- **Dependency:** Defines the execution order between tasks.
- **Run:** A single execution of a Job or Task.
- **DAG (Directed Acyclic Graph):** Represents tasks and their dependencies.

## 2. Tasks

A Task represents an operation within a Job.

Examples:

- Execute a notebook.
- Run a Python script.
- Execute a SQL query.
- Run another supported task type.

Each Task can have its own configuration, parameters and dependencies.

## 3. Task Dependencies

Dependencies determine when a task can execute.

Example:

```text
Task A ──> Task B ──> Task C
```

- Task A executes first.
- Task B starts after Task A completes successfully.
- Task C starts after Task B completes successfully.

### Parallel execution

Independent tasks can execute in parallel.

```text
          ┌──> Task A ──┐
Job ──────┼──> Task B ──┼──> Task D
          └──> Task C ──┘
```

Task D waits for all three upstream tasks to complete successfully.

## 4. Reusing Notebooks

A single notebook can be reused by multiple Tasks.

Example: six CSV files are ingested using the same notebook.

| Task | Source file | Target table |
|---|---|---|
| Task 1 | customers.csv | customers |
| Task 2 | products.csv | products |
| Task 3 | orders.csv | orders |
| Task 4 | orders_items.csv | orders_items |
| Task 5 | payments.csv | payments |
| Task 6 | refunds.csv | refunds |

Each Task passes different parameters to the same notebook.

This avoids duplicating code and makes workflows easier to maintain.

## 5. Job Execution

A Job can be started in different ways:

- Manually using Run Now.
- Automatically using a schedule.
- Through a File Arrival trigger.
- Through a Table Update trigger.
- Using a Continuous trigger.

## 6. Practical Example: Sales Ingestion

Project: `sales_ingestion_job`

Objective: ingest six CSV files from a Unity Catalog Volume and save them as managed Delta tables.

Source location:

```text
/Volumes/first_catalog/default/my_volume/
```

Target tables:

```text
first_catalog.default.customers
first_catalog.default.products
first_catalog.default.orders
first_catalog.default.orders_items
first_catalog.default.payments
first_catalog.default.refunds
```

The Job uses six Tasks that execute the same ingestion notebook with different parameters.

Independent ingestion tasks can run in parallel.

## 7. Important Concepts

| Concept | Purpose |
|---|---|
| Job | Orchestrates the complete workflow |
| Task | Executes an individual operation |
| Dependency | Controls execution order |
| DAG | Represents the workflow structure |
| Parallel execution | Runs independent tasks simultaneously |
| Run | Represents an execution instance |

## 8. Key Takeaways

- Lakeflow Jobs orchestrates data workflows.
- A Job can contain multiple Tasks.
- Tasks can depend on other Tasks.
- Independent Tasks can run in parallel.
- A single notebook can be reused with different parameters.
- Dependencies control execution order.
