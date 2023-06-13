from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def parse_json(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        col("key"), 
        from_json(col("value"), "channel STRING, ts STRING, text STRING, source STRING").alias("value_parsed")
    )
