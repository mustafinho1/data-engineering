from pyspark.sql import functions as F
def transform_sales(dataframes):
    orders_df = dataframes["orders.csv"]
    payments_df = dataframes["payments.csv"]
    refunds_df = dataframes["refunds.csv"]
    payments_clean = payments_df.filter(
    F.col("payment_status") == "succeeded"
    )
    payments_clean = payments_clean.select(
    "order_id",
    "payment_id",
    "payment_method",
    "amount"
    )
    sales = orders_df.join(
    payments_clean,
    "order_id",
    "left"
    )
    refunds_clean = refunds_df.select(
    "payment_id",
    "refund_id",
    "refund_reason",
    "amount"
    
    
    )
    refunds_clean = refunds_clean.withColumnRenamed(
    "amount",
    "refund_amount"
    )
    sales = sales.join(
    refunds_clean,
    "payment_id",
    "left"
    )
    sales = sales.withColumn(
    "net_sales",
    F.when(
        F.col("payment_id").isNull(),
        F.lit(0.0)
    ).otherwise(
        F.round(
            F.col("order_total") -
            F.coalesce(F.col("refund_amount"), F.lit(0.0)),
            2
        )
    )
    )
    return sales
def get_unprocessed_sales(sales, historical):
   if historical is None:
       return sales 
   else:
    new_sales = sales.join(
        historical,
        "order_id",
        "left_anti"
    )
    return new_sales 
    