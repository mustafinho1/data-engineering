required_columns = {
    "customers.csv": [
        "customer_id",
        "created_at",
        "country_code",
        "acquisition_channel",
        "customer_segment"
    ],

    "products.csv": [
        "product_id",
        "sku",
        "product_name",
        "category",
        "unit_cost",
        "list_price"
    ],

    "orders.csv": [
        "order_id",
        "customer_id",
        "ordered_at",
        "order_status",
        "currency",
        "subtotal",
        "tax_amount",
        "shipping_amount",
        "order_total"
    ],

    "refunds.csv": [
        "refund_id",
        "payment_id",
        "order_id",
        "refunded_at",
        "refund_reason",
        "amount"
    ],

    "payments.csv": [
        "payment_id",
        "order_id",
        "paid_at",
        "payment_method",
        "payment_status",
        "amount"
    ],

    "order_items.csv": [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_amount",
        "line_total"
    ]
}

class DataQualityError(Exception):
    pass
def validate_file(df, file):
    required = required_columns[file.name]
    for column in required:
        if column not in df.columns:
            raise DataQualityError(f"Missing columns required:{column}")
    return df, True

