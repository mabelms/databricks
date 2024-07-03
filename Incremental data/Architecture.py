# Databricks notebook source
# MAGIC %run ../Funtions/Datasets

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

archivos = dbutils.fs.ls("dbfs:/mnt/demo-datasets/bookstore/orders-raw/")

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
    .load(f"{dataset_bookstore}/sessions-raw")
    .createOrReplaceTempView("sessions_raw_temp"))