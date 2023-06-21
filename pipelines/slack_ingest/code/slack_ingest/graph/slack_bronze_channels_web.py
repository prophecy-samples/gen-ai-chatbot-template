from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_ingest.config.ConfigStore import *
from slack_ingest.udfs.UDFs import *

def slack_bronze_channels_web(spark: SparkSession) -> DataFrame:
    from spark_ai.webapps.slack import SlackUtilities
    from pyspark.dbutils import DBUtils

    return SlackUtilities(
          token = DBUtils(spark).secrets.get(scope = "slack", key = "token"),
          spark = spark,
          path_tmp = "dbfs:/tmp/slack_data/",
          limit = -1
        )\
        .read_channels()
