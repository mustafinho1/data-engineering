
# Retries and Notifications in Lakeflow Jobs

## 1. Retries

Retries allow a failed task to execute again automatically.

They are useful when failures may be temporary, such as:

- Temporary network problems.
- External service interruptions.
- Transient infrastructure errors.

A retry does not guarantee that the task will succeed.

## 2. Retry Configuration

Retries can be configured for a task.

Common configuration options include:

- Maximum number of retries.
- Minimum time between retries.
- Whether to retry after a failure.

The exact configuration depends on the Job settings available in the workspace.

## 3. What Happens When a Task Fails?

Imagine this workflow:

Task A → Task B → Task C

If Task B fails:

1. Databricks evaluates the retry configuration.
2. If retries are configured, Task B can execute again.
3. If Task B eventually succeeds, Task C can run.
4. If Task B exhausts its retries and remains unsuccessful, dependent tasks normally do not run.

Task A does not need to run again just because Task B is retried.

## 4. Notifications

Notifications inform users about Job or task execution events.

They can be configured at different levels.

### Job-level notifications

These notify users about the overall Job outcome.

Examples:

- Job run failure.
- Job run success.
- Job duration warning, when configured and supported.

### Task-level notifications

These notify users about events related to an individual task.

They are useful when a specific task is particularly important.

## 5. Job Notifications vs Task Notifications

| Feature | Job-level | Task-level |
|---|---|---|
| Scope | Entire Job | Individual Task |
| Purpose | Monitor overall workflow | Monitor a specific task |
| Example | Job run fails | Ingestion task fails |

Important: A task may fail initially but succeed after retries. The final Job outcome can therefore be successful.

Do not assume that a Job-level failure notification is sent if the Job ultimately succeeds.

## 6. Practical Example

Consider the following workflow:

Task A: Ingest customers  
Task B: Ingest orders  
Task C: Transform sales

If Task B fails because of a temporary network problem:

- Databricks retries Task B if configured.
- If Task B succeeds on a retry, Task C can execute.
- If Task B ultimately fails, the Job may finish with a failed outcome.
- Configured notifications communicate the relevant execution events.

## 7. Key Takeaways

- Retries automatically repeat failed task executions when configured.
- Retries are useful for temporary failures.
- A successful retry allows downstream tasks to continue when dependencies are satisfied.
- Job-level notifications concern the overall workflow.
- Task-level notifications concern individual tasks.
- Always distinguish an initial failure from the final execution outcome.
