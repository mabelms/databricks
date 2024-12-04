# Databricks notebook source
# MAGIC %md
# MAGIC #### Extracción (Extraction)
# MAGIC

# COMMAND ----------

# Importar las bibliotecas necesarias
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Configurar la sesión de Spark en Databricks
spark = SparkSession.builder.appName("ETLExample").getOrCreate()

# URL del conjunto de datos público en formato CSV
url_datos = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# Descargar datos desde la URL
respuesta = requests.get(url_datos)
datos_csv = respuesta.text.splitlines()


# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformación (Transformation)

# COMMAND ----------


# Crear un DataFrame Spark a partir de los datos CSV
columnas = ["sepal_length", "sepal_width", "petal_length", "petal_width", "class"]
datos_spark = spark.createDataFrame([tuple(line.split(',')) for line in datos_csv]).toDF(*columnas)

# Realizar algunas transformaciones simples (cambiar tipos de datos, etc.)
datos_transformados = datos_spark.withColumn("sepal_length", col("sepal_length").cast("double"))
datos_transformados = datos_transformados.withColumn("sepal_width", col("sepal_width").cast("double"))
datos_transformados = datos_transformados.withColumn("petal_length", col("petal_length").cast("double"))
datos_transformados = datos_transformados.withColumn("petal_width", col("petal_width").cast("double"))


# COMMAND ----------

# MAGIC %md
# MAGIC ### Carga (Loading)

# COMMAND ----------


# Especificar la ruta de destino en DBFS
ruta_destino_dbfs = "/dbfs/tmp/etl/"
dataset_bookstore = 'dbfs:/mnt/demo-datasets/bookstore'

# Guardar los datos transformados en formato Parquet en DBFS
# datos_transformados.write.format("parquet").save(ruta_destino_dbfs)
datos_transformados.createOrReplaceTempView("datos_transformados_v")

## Puedes usar la vista temporal en consultas posteriores
resultado = spark.sql("SELECT * FROM datos_transformados_v")
resultado.show()


# COMMAND ----------

# MAGIC %md
# MAGIC #### DBFS

# COMMAND ----------

# Especifica la ruta del directorio que deseas listar
ruta_directorio = "dbfs:/databricks-datasets/"

# Utiliza dbutils.fs.ls() para listar los archivos y carpetas en la ubicación especificada
archivos = dbutils.fs.ls(ruta_directorio)

# Imprime los nombres de los archivos y carpetas
for archivo in archivos:
    print(archivo.path)


# COMMAND ----------

######### crear carpeta
# Especifica la ruta de la carpeta que deseas crear
ruta_carpeta = "/mnt/dbfs/nueva_carpeta"

dbutils.fs.mkdirs(ruta_carpeta)

#borrar archivo

#listar


#copiar


archivos = dbutils.fs.ls(ruta_destino_dbfs)
# Imprime los nombres de los archivos
for archivo in archivos:
    print(archivo.path)

# Especifica la ruta del directorio que deseas limpiar
ruta_directorio = ruta_destino_dbfs

# Utiliza dbutils.fs.rm() para limpiar el directorio
dbutils.fs.rm(ruta_directorio, recurse=True)


# COMMAND ----------

# Listar archivos en un directorio en DBFS
dbutils.fs.ls("/dbfs/tmp/etl/")


# COMMAND ----------

# MAGIC %fs mkdirs /dbfs/tmp/etl/extraccion
# MAGIC