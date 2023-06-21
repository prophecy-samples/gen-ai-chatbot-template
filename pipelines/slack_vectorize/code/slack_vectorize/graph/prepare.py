from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def prepare(spark: SparkSession, slack_silver_conversations_vectorized_1: DataFrame) -> DataFrame:
    return slack_silver_conversations_vectorized_1.select(
        col("id"), 
        col("text").alias("content_chunk"), 
        col("embedding"), 
        lit(None).cast(StringType()).alias("url")
    )
