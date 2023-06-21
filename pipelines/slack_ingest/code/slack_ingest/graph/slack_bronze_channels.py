from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_ingest.config.ConfigStore import *
from slack_ingest.udfs.UDFs import *

def slack_bronze_channels(spark: SparkSession, slack_bronze_channels_web: DataFrame):
    slack_bronze_channels_web.write\
        .format("delta")\
        .option("mergeSchema", True)\
        .option("overwriteSchema", True)\
        .mode("overwrite")\
        .saveAsTable(f"prophecy_data.slack_bronze.channels")
