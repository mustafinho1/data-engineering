
# Triggers and Scheduling in Lakeflow Jobs

## 1. What are Triggers?

Triggers define when a Lakeflow Job starts executing.

They allow workflows to run automatically without requiring manual execution.

## 2. Manual Trigger

A Job can be started manually using the Run Now option.

Typical use cases:

- Testing a Job.
- Running a workflow on demand.
- Executing a process after a manual intervention.

## 3. Scheduled Trigger

A Scheduled Trigger starts a Job according to a predefined schedule.

Examples:

- Every day at 02:00.
- Every hour.
- Every Monday.
- At a specific interval.

Typical use cases:

- Daily ETL pipelines.
- Scheduled reporting.
- Periodic data processing.

## 4. File Arrival Trigger

A File Arrival Trigger starts a Job when new files are detected in a configured cloud storage location.

Typical use cases:

- Processing incoming CSV files.
- Ingesting daily JSON deliveries.
- Processing files uploaded by external systems.

Important considerations:

- Databricks monitors the configured location.
- Detection is based on configured monitoring settings.
- Multiple arriving files may be processed in the same Job run.
- It does not necessarily start one execution per file.

## 5. Table Update Trigger

A Table Update Trigger starts a Job when a configured table is updated and the trigger conditions are met.

Typical use cases:

- Starting transformations after source tables change.
- Updating downstream datasets.
- Reacting to changes in upstream data.

## 6. Continuous Trigger

A Continuous Trigger keeps a Job running continuously.

When a run finishes, Databricks can start another run according to the continuous execution behavior.

Typical use cases:

- Continuous data processing.
- Workloads that need ongoing execution.
- Streaming-related workflows.

## 7. Trigger Comparison

| Trigger | When it starts |
|---|---|
| Manual | When a user starts the Job |
| Scheduled | At configured times or intervals |
| File Arrival | When new files are detected |
| Table Update | When configured table updates meet the conditions |
| Continuous | Maintains continuous execution |

## 8. Choosing the Right Trigger

Examples:

- Daily ingestion at 02:00 → Scheduled.
- New CSV files arrive in cloud storage → File Arrival.
- A source table is updated → Table Update.
- A continuously running workload → Continuous.
- Run a workflow manually for testing → Manual.

## 9. Key Takeaways

- Triggers determine when Jobs execute.
- Scheduled triggers are time-based.
- File Arrival triggers monitor storage locations.
- Table Update triggers react to table changes.
- Continuous triggers support ongoing execution.
- Manual execution is useful for testing and on-demand processing.
