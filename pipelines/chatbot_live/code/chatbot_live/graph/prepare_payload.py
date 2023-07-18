from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def prepare_payload(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(col("channel"), col("ts"), col("openai_answer.choices")[0].alias("answer"))
