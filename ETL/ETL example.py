# Databricks notebook source
# MAGIC %pip install seaborn

# COMMAND ----------

from pyspark.sql import SparkSession
import seaborn as sns
import pandas as pd
from pyspark.sql.functions import sum, col

# Create a sample DataFrame with seaborn
df_seaborn = sns.load_dataset("tips")

# Initialize the Spark session
spark = SparkSession.builder.appName("ETLExample").getOrCreate()

# Convert the pandas DataFrame to a Spark DataFrame
df_spark = spark.createDataFrame(df_seaborn)

# Transformation: Calculate total sales per product
df_transformed = df_spark.groupBy("day").agg(sum(col("total_bill").cast("double")).alias("total_sales"))

# Specify the Parquet file path
parquet_path = "/dbfs/tmp/etl/seaborn/results.parquet"
df_transformed.write.parquet(parquet_path, mode="overwrite")

# Read Parquet files into a DataFrame
df_read = spark.read.parquet(parquet_path)

# Show the contents of the DataFrame
df_read.show()


# COMMAND ----------

# MAGIC %md
# MAGIC ### Extract

# COMMAND ----------

# Databricks-specific command to create a Spark session
spark = SparkSession.builder.appName("ETLExample").getOrCreate()

def extract_data(dataset_name):
    df_seaborn = sns.load_dataset("tips")
    df_spark = spark.createDataFrame(df_seaborn)
    return df_spark

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transform

# COMMAND ----------

def transform_data(df):
    df_transformed = df.withColumn("sex_numeric", when(col("sex") == "Male", "1").otherwise("0"))
    df_transformed = df_transformed.fillna(0, subset=["total_bill", "tip"])
    df_transformed = df_transformed.groupBy("day", "sex_numeric").agg(
        sum(col("total_bill").cast("double")).alias("total_sales"),
        avg(col("tip").cast("double")).alias("avg_tip")
    )
    df_transformed = df_transformed.withColumn("tip_percentage", col("avg_tip") / col("total_sales") * 100)
    return df_transformed


# COMMAND ----------

# MAGIC %md
# MAGIC ### Load

# COMMAND ----------


def write_parquet(df_transformed, output_path):
    df_transformed.write.parquet(parquet_path, mode="overwrite")    

# COMMAND ----------

# Crear una carpeta llamada 'manage_files' en DBFS
dbutils.fs.mkdirs("dbfs:/manage_files")
dbutils.fs.mkdirs("dbfs:/manage_files/etl")
dbutils.fs.mkdirs("dbfs:/manage_files/etl/seaborn")

# COMMAND ----------

def main():
    dataset_name = "tips"
    df_source = extract_data(dataset_name)
    df_transformed = transform_data(df_source)

    parquet_path = "dbfs:/manage_files/etl/seaborn/results.parquet"
    write_parquet(df_transformed, parquet_path)
    
    df_read = spark.read.parquet(parquet_path)
    df_read.show()

if __name__ == "__main__":
    main()

# COMMAND ----------

dbutils.fs.ls("dbfs:/manage_files/etl/seaborn/")