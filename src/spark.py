from pyspark.sql import SparkSession 
spark = SparkSession.builder \
    .appName("Retail") \
    .master("local[*]") \
    .config("spark.driver.host", "127.0.0.1") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()