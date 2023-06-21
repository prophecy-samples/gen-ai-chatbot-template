from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def clean(spark: SparkSession, Join_1_1: DataFrame) -> DataFrame:
    return Join_1_1.filter((col("sub_thread_ts").isNotNull() & (col("text") != lit("This message was deleted."))))
