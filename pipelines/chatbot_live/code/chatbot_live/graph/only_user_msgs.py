from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def only_user_msgs(spark: SparkSession, Script_1: DataFrame) -> DataFrame:
    return Script_1.filter((col("value_parsed.source") == lit("user")))
