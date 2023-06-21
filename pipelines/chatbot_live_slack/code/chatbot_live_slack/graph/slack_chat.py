from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live_slack.config.ConfigStore import *
from chatbot_live_slack.udfs.UDFs import *

def slack_chat(spark: SparkSession) -> DataFrame:
    from pyspark.dbutils import DBUtils

    return spark.readStream\
        .format("io_prophecy.spark_ai.webapps.slack.SlackSourceProvider")\
        .option("token", DBUtils(spark).secrets.get(scope = "slack", key = "app_token"))\
        .load()
