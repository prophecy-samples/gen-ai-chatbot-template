from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def rename(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(col("id"), col("openai_embedding").alias("embedding"), col("content_chunk"), col("url"))
