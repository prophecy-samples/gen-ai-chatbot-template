from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def content_vectors(spark: SparkSession, vectorize: DataFrame):
    vectorize.write\
        .format("delta")\
        .option("mergeSchema", True)\
        .option("overwriteSchema", True)\
        .mode("overwrite")\
        .saveAsTable(f"prophecy_data.web_silver.content_vectorized")
