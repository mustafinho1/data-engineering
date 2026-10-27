import logging
from src.spark import spark
from src.config import csv_folder, parquet_folder, processed_files 

def get_files():
    if not csv_folder.exists() or not csv_folder.is_dir():
        raise FileNotFoundError(
            f"Input folder does not exist: {csv_folder}"
        )

    files = list(csv_folder.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No CSV files found in: {csv_folder}"
        )
        

    return files

def process_file(file_path):
    try:
        df = spark.read.csv(
            str(file_path),
            header=True,
            inferSchema=True
        )
        
        if not df.columns:
            raise ValueError("CSV has no columns")

        return df, True

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        return None, False
def load_historical_sales():
    if parquet_folder.exists():
        return spark.read.parquet(str(parquet_folder))
    else:
        return None
        
def save_sales_parquet(new_sales):
    if new_sales.isEmpty():
        logging.info("No new sales to save.")
        return

    mode = "append" if parquet_folder.exists() else "overwrite"

    new_sales.write \
        .mode(mode) \
        .parquet(str(parquet_folder))

    logging.info(f"Sales saved to Parquet using mode: {mode}")

def get_processed_files():
    if not processed_files.exists():
        return set()

    with open(processed_files, "r") as f:
        return set(f.read().splitlines())   

def register_processed_file(file_path):
    with open(processed_files, "a") as f:
        f.write(f"{file_path.name}\n")