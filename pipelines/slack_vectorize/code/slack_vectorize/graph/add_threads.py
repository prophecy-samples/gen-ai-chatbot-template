from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def add_threads(spark: SparkSession, conversations: DataFrame, subconversations: DataFrame, ) -> DataFrame:
    return conversations\
        .alias("conversations")\
        .join(
          subconversations.alias("subconversations"),
          (col("conversations.ts") == col("subconversations.thread_ts")),
          "left_outer"
        )\
        .select(col("conversations.channel_id").alias("channel_id"), col("conversations.ts").alias("ts"), col("conversations.text").alias("text"), col("conversations.thread_ts").alias("thread_ts"), col("subconversations.ts").alias("sub_ts"), col("subconversations.text").alias("sub_text"), col("subconversations.thread_ts").alias("sub_thread_ts"))
