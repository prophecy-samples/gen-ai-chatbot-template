from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def collect_results(spark: SparkSession, Watermark_1: DataFrame) -> DataFrame:
    df1 = Watermark_1.groupBy(window(col("created_at"), "1 second").alias("created_at"), col("ts"), col("channel"))

    return df1.agg(
        array_join(collect_list(col("content_chunk")), "; ").alias("content_chunk"), 
        first(col("input")).alias("input")
    )
