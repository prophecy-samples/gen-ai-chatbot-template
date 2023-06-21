from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def group_threads(spark: SparkSession, Filter_1: DataFrame) -> DataFrame:
    df1 = Filter_1.groupBy(col("channel_id"), col("ts"))

    return df1.agg(
        first(col("text")).alias("text"), 
        collect_list(col("sub_ts")).alias("sub_tss"), 
        collect_list(col("sub_text")).alias("sub_texts")
    )
