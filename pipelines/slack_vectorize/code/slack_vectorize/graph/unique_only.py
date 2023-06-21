from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def unique_only(spark: SparkSession, Filter_3: DataFrame) -> DataFrame:
    return Filter_3.dropDuplicates(["channel_id", "ts"])
