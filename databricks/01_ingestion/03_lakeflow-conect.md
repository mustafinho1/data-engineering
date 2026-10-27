# Lakeflow Connect in Databricks

## 1. What is Lakeflow Connect?

Lakeflow Connect is Databricks' data ingestion solution for connecting external data sources to the Databricks Lakehouse.

It provides managed connectors that reduce the amount of custom ingestion code and infrastructure that data engineers need to maintain.

It supports several categories of sources, including:

- Enterprise SaaS applications, such as Salesforce and HubSpot.
- Relational databases, such as MySQL, PostgreSQL, Oracle, and SQL Server, depending on connector availability.
- Enterprise file services, such as Google Drive and SharePoint.
- Streaming sources, such as Apache Kafka and RabbitMQ.

**Main use case:** ingesting data from external business systems into Databricks with less custom code and operational overhead.

Official documentation: https://docs.databricks.com/aws/en/ingestion/overview

## 2. Why use Lakeflow Connect?

Managed connectors can provide:

- **Managed authentication:** handle source-specific authentication using configured connections.
- **Incremental ingestion:** ingest new or changed data instead of repeatedly copying everything, where supported.
- **Change Data Capture (CDC):** capture changes from supported databases.
- **Schema evolution:** handle supported schema changes according to the connector's capabilities.
- **Automatic retries:** retry certain failures without requiring custom retry logic.
- **Monitoring:** expose pipeline health and ingestion information.
- **Unity Catalog governance:** manage access to connections and destination data.
- **Reduced maintenance:** Databricks manages much of the connector implementation and its operational lifecycle.

Not every connector supports every feature. Connector availability, supported interfaces, and release status vary by source.

## 3. How does Lakeflow Connect work?

A typical managed ingestion pipeline involves these components:

1. **Source system:** the application, database, or service containing the data.
2. **Connection:** stores the authentication and connection configuration.
3. **Ingestion pipeline:** reads data from the source and processes it incrementally when supported.
4. **Destination tables:** store the ingested data in Databricks.

For database connectors, additional components such as an ingestion gateway and staging storage may be required.

The pipeline can then be scheduled or orchestrated using Lakeflow Jobs.

## 4. Example: ingesting Salesforce data

Imagine a company stores customer information in Salesforce and wants to analyze it in Databricks.

A typical workflow is:

1. Configure a connection to Salesforce.
2. Select the objects or data to ingest, subject to connector support.
3. Configure the ingestion pipeline and destination.
4. Run the initial ingestion.
5. Schedule subsequent runs to capture new or changed data.
6. Use the destination tables in SQL queries, transformations, and analytics.

The initial run typically loads the selected data. Subsequent runs use the connector's supported incremental mechanism to retrieve changes.

The precise configuration depends on the Salesforce connector and its current capabilities.

## 5. Database connectors: CDC vs. query-based ingestion

Lakeflow Connect supports different approaches for ingesting relational database data.

### Change Data Capture (CDC)

CDC captures database changes, such as inserts, updates, and deletes, using supported source mechanisms.

It is useful when the destination needs to reflect changes made in the source without repeatedly extracting entire tables.

For example:

- A customer is inserted.
- A customer's address is updated.
- An order is deleted.

A CDC-enabled pipeline can capture these changes when supported and configured correctly.

### Query-based ingestion

Query-based connectors query the source database directly on a schedule instead of requiring CDC infrastructure.

They can use a **cursor column**, such as a timestamp or monotonically increasing integer, to identify new or changed rows.

This approach depends on the source schema and the cursor column's behavior. Changes that cannot be detected through the chosen cursor may require a different ingestion strategy.

Official documentation: https://docs.databricks.com/aws/en/ingestion/lakeflow-connect/query-based-overview

## 6. Lakeflow Connect vs. Auto Loader vs. COPY INTO

| Feature | Lakeflow Connect | Auto Loader | COPY INTO |
|---|---|---|---|
| Primary purpose | Managed ingestion from supported external sources | Incremental file ingestion | SQL-based incremental file loading |
| Typical sources | SaaS applications, databases, supported file and streaming services | Files in supported cloud storage | Files in supported cloud storage |
| Custom code | Often minimal for managed connectors | Requires configuring a streaming ingestion pipeline | Uses SQL |
| CDC | Available for supported database connectors | Not its primary purpose | Not its primary purpose |
| File discovery | Depends on connector type | Designed for scalable discovery of new files | Tracks files loaded by the command |
| Best fit | Supported business applications and databases | Large or growing collections of files | Straightforward SQL-driven file ingestion |

These tools are complementary rather than direct replacements for every use case.

For example, if a company receives CSV files in a cloud storage directory, Auto Loader may be appropriate. If it needs to ingest customer records from Salesforce, a managed Lakeflow Connect connector may be a better fit.

## 7. Lakeflow Connect vs. Lakeflow Jobs vs. Lakeflow Spark Declarative Pipelines

These names refer to different capabilities within the Lakeflow data engineering platform.

### Lakeflow Connect

Focuses on ingesting data from external sources through connectors.

### Lakeflow Jobs

Focuses on orchestration: scheduling and coordinating tasks such as notebooks, pipelines, and other supported workloads.

### Lakeflow Spark Declarative Pipelines

Provides a declarative framework for defining and maintaining batch and streaming data pipelines using SQL and Python.

**Remember:** Connect brings data in; Jobs orchestrates work; Spark Declarative Pipelines defines data processing pipelines.

Official documentation: https://docs.databricks.com/aws/en/data-engineering/

## 8. Advantages and limitations

### Advantages

- Less custom connector code.
- Managed authentication and source-specific integration.
- Incremental ingestion where supported.
- Integration with Unity Catalog and other Databricks capabilities.
- Monitoring and automatic retries for supported failure scenarios.

### Limitations

- Not every source has a managed connector.
- Connector capabilities and availability vary.
- Source APIs, permissions, rate limits, and network access can affect ingestion.
- Managed services still incur costs.
- Some database connectors require additional infrastructure and source-side configuration.
- Custom ingestion may be necessary when the required source or behavior is unsupported.

If a managed connector does not meet the requirements, consider Lakeflow pipelines, Structured Streaming, SQL/Spark APIs, or a custom connector.

## 9. Practical checklist before using a connector

Before implementing a pipeline, verify:

- Is the source supported by a managed connector?
- Is the connector generally available or in a preview release?
- Which authentication method does it require?
- Does it support incremental ingestion, CDC, or only full loads?
- Which source objects and data types are supported?
- What permissions and networking configuration are needed?
- Where will the destination tables be stored?
- How will the pipeline be scheduled, monitored, and billed?

Official connector overview: https://docs.databricks.com/aws/en/ingestion/lakeflow-connect

## 10. Key takeaways

- Lakeflow Connect simplifies ingestion from supported external systems.
- Managed connectors reduce the need to maintain custom extraction logic.
- CDC captures database changes where supported.
- Query-based ingestion can use a cursor column to identify new or changed rows.
- Unity Catalog helps govern connections and destination data.
- Lakeflow Connect, Lakeflow Jobs, and Lakeflow Spark Declarative Pipelines have distinct roles.
- Always check the documentation for the specific connector because capabilities and availability vary.
