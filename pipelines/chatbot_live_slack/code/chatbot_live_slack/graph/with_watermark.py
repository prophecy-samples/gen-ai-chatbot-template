from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live_slack.config.ConfigStore import *
from chatbot_live_slack.udfs.UDFs import *

def with_watermark(spark: SparkSession, with_original_content: DataFrame) -> DataFrame:
    return with_original_content.withWatermark("created_at", "1 second")
