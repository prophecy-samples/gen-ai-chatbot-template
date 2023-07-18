from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def slack_chat(spark: SparkSession) -> DataFrame:
    from pyspark.dbutils import DBUtils

    return spark.readStream\
        .format("io.prophecy.spark_ai.webapps.slack.SlackSourceProvider")\
        .option("token", DBUtils(spark).secrets.get(scope = "slack", key = "app_token"))\
        .load()
