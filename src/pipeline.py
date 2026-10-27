
import logging

from src.ingestion import (
    get_files,
    process_file,
    load_historical_sales,
    save_sales_parquet,
    get_processed_files,
    register_processed_file,
)
from src.validation import validate_file, DataQualityError
from src.transformation import transform_sales, get_unprocessed_sales


def run_pipeline():
    files = get_files()
    processed = get_processed_files()
    dataframes = {}

    for file in files:
        logging.info(f"Processing file: {file.name}")

        df, success = process_file(file)
        if not success:
            raise RuntimeError(f"Could not read {file.name}")

        try:
            df, success = validate_file(df, file)
        except DataQualityError as e:
            logging.error(e)
            raise

        dataframes[file.name] = df

    sales = transform_sales(dataframes)

    historical = load_historical_sales()
    new_sales = get_unprocessed_sales(sales, historical)

    save_sales_parquet(new_sales)

    for file in files:
        if file.name not in processed:
            register_processed_file(file)

    logging.info("Pipeline completed successfully.")
    return new_sales
        
        
        