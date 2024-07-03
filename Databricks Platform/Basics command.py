# Databricks notebook source
# MAGIC %md  
# MAGIC #####Listar

# COMMAND ----------

#Listar
ruta_directorio = "dbfs:/FileStore/shared_uploads/mabelcruzcadillo@gmail.com/log_csv/local"

# Utiliza dbutils.fs.ls() para listar los archivos y carpetas en la ubicación especificada
archivos = dbutils.fs.ls(ruta_directorio)

# Imprime los nombres de los archivos y carpetas
for archivo in archivos:
    print(archivo.path)


# COMMAND ----------

# MAGIC %md
# MAGIC ####crear carpeta

# COMMAND ----------

# Especifica la ruta de la carpeta que deseas crear
ruta_carpeta = "dbfs:/FileStore/shared_uploads/mabelcruzcadillo@gmail.com/log_csv/local"

# Utiliza dbutils.fs.mkdirs() para crear la carpeta
dbutils.fs.mkdirs(ruta_carpeta)


# COMMAND ----------

# MAGIC %md
# MAGIC ####Eliminar carpeta

# COMMAND ----------

# Especifica la ruta de la carpeta que deseas eliminar
ruta_carpeta = "dbfs:/FileStore/shared_uploads/mabelcruzcadillo@gmail.com/log_csv/local/"

# Utiliza dbutils.fs.rm() para eliminar la carpeta
dbutils.fs.rm(ruta_carpeta, recurse=True)


# COMMAND ----------

# MAGIC %md
# MAGIC ####copiar archivos

# COMMAND ----------

# Especifica la ruta de origen y destino del archivo que deseas copiar
ruta_origen = "/portafolio/dbfs/datasets/archivo.txt"
ruta_destino = "/portafolio/dbfs/dataset/archivo_destino.txt"

# Utiliza dbutils.fs.cp() para copiar el archivo
dbutils.fs.cp(ruta_origen, ruta_destino)


# COMMAND ----------

# MAGIC %md
# MAGIC ##### Dataset

# COMMAND ----------

import os
import requests

# Hacer el request y obtener los datos
response = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
datos = response.text

# Especificar la ruta y nombre del archivo en DBFS
ruta_carpeta = '/portafolio/dbfs/datasets/'
ruta_archivo = 'archivo.txt'

# Crear la carpeta si no existe
os.makedirs(ruta_carpeta, exist_ok=True)

# Escribir los datos en un archivo en DBFS
with open(os.path.join(ruta_carpeta, ruta_archivo), 'w') as f:
    f.write(datos)

print("Archivo creado exitosamente en DBFS:", os.path.join(ruta_carpeta, ruta_archivo))

archivos = dbutils.fs.ls(ruta_carpeta)
