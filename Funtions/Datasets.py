# Databricks notebook source
def path_exists(path):
  try:
    dbutils.fs.ls(path)
    return True
  except Exception as e:
    if 'java.io.FileNotFoundException' in str(e):
      return False
    else:
      raise

# COMMAND ----------

def download_dataset(source, target):
    files = dbutils.fs.ls(source)

    for f in files:
        source_path = f"{source}/{f.name}"
        target_path = f"{target}/{f.name}"
        if not path_exists(target_path):
            print(f"Copying {f.name} ...")
            dbutils.fs.cp(source_path, target_path, True)


# COMMAND ----------


#data_source_uri = "wasbs://resources@datasetsmc.blob.core.windows.net/datasets/bookstore/"
#dataset_bookstore = 'dbfs:/portafolio/datasets/bookstore'
data_source_uri = "wasbs://resources@datasetsmc.blob.core.windows.net/datasets/gym_sessions/"
dataset_bookstore = "dbfs:/portafolio/datasets/gym_sessions/"
spark.conf.set(f"dataset.bookstore", dataset_bookstore)

# COMMAND ----------

download_dataset(data_source_uri, dataset_bookstore)