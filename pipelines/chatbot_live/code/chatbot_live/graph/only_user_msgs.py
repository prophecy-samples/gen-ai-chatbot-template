from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def only_user_msgs(spark: SparkSession, Script_1: DataFrame) -> DataFrame:
    return Script_1.filter(
        (col("value_parsed").isNotNull() & (col("value_parsed.payload.event.user") != lit("U05AU1K4ELV")))
    )
