from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def collect_context(spark: SparkSession, Join_1: DataFrame) -> DataFrame:
    df1 = Join_1.groupBy(window(col("ts_ts"), "2 seconds").alias("ts_ts"))

    return df1.agg(
        array_join(collect_list(col("content_chunk")), "; ").alias("context"), 
        first(col("input")).alias("input"), 
        first(col("ts")).alias("ts"), 
        first(col("channel")).alias("channel")
    )
