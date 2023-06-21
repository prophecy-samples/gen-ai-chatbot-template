from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def merge_msgs(spark: SparkSession, OrderBy_1_1: DataFrame) -> DataFrame:
    return OrderBy_1_1.select(
        concat(lit("slack-"), col("channel_id"), lit("."), col("ts")).alias("id"), 
        col("channel_id"), 
        col("ts"), 
        concat(col("text"), lit("; "), array_join(col("sub_texts"), "; ")).alias("text")
    )
