from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *

def in_100_parts(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.repartition(100)
