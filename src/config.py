from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent
csv_folder = base_dir/"data"/"raw"
parquet_folder = base_dir/"data"/"ventas_parquet"
processed_files = base_dir/"data"/"processed_files.txt"