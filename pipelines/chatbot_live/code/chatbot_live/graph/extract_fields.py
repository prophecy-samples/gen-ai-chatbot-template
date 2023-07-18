from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def extract_fields(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        col("value_parsed.payload.event.text").alias("text"), 
        col("value_parsed.payload.event.ts").alias("ts"), 
        col("value_parsed.payload.event.user").alias("user"), 
        col("value_parsed.payload.event.channel").alias("channel"), 
        from_unixtime(col("value_parsed.payload.event.ts")).cast(TimestampType()).alias("created_at")
    )
