from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def bot_messages_target(spark: SparkSession, in0: DataFrame):
    from pyspark.dbutils import DBUtils
    from spark_ai.webapps.slack import SlackUtilities
    SlackUtilities(token = DBUtils(spark).secrets.get(scope = "slack", key = "token"), spark = spark)\
        .write_messages(in0)
