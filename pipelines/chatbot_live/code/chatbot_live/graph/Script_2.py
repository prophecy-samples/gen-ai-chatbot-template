from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def Script_2(spark: SparkSession, in0: DataFrame) -> DataFrame:
    out0 = in0.withColumn("ts_ts", expr("current_timestamp()")).withWatermark("ts_ts", "2 seconds")

    return out0
