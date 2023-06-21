from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def rename(spark: SparkSession, OpenAI_1: DataFrame) -> DataFrame:
    return OpenAI_1.select(
        col("id"), 
        col("channel_id"), 
        col("ts"), 
        col("text"), 
        col("openai_embedding").alias("embedding"), 
        col("openai_error").alias("error")
    )
