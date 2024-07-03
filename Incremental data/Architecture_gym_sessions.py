# Databricks notebook source
# MAGIC %md
# MAGIC ###DBFS

# COMMAND ----------

# MAGIC %run ../Funtions/Datasets_gym_sessions

# COMMAND ----------

#Listar
#ruta_directorio = "dbfs:/portafolio/datasets/bookstore/"
ruta_directorio = "dbfs:/portafolio/datasets/gym_sessions/"
# Utiliza dbutils.fs.ls() para listar los archivos y carpetas en la ubicación especificada
archivos = dbutils.fs.ls(ruta_directorio)

# Imprime los nombres de los archivos y carpetas
for archivo in archivos:
    print(archivo.path)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Auto Loader

# COMMAND ----------

(spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "parquet")
    .option("cloudFiles.schemaLocation", "dbfs:/portafolio/demo/checkpoints/sessions_raw")
    .load(f"{dataset_gym_sessions}/sessions-raw/")
    .createOrReplaceTempView("sessions_raw_temp"))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW sessions_tmp AS (
# MAGIC   SELECT *, current_timestamp() arrival_time, input_file_name() source_file
# MAGIC   FROM sessions_raw_temp
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sessions_tmp

# COMMAND ----------

# MAGIC %md
# MAGIC ## Creating Bronze Table

# COMMAND ----------

(spark.table("sessions_tmp")
      .writeStream
      .format("delta")
      .option("checkpointLocation", "dbfs:/portafolio/demo/checkpoints/sessions_bronze")
      .outputMode("append")
      .table("sessions_bronze"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM sessions_bronze

# COMMAND ----------

load_new_data()