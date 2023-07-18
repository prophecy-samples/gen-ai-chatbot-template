from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def with_watermark(spark: SparkSession, with_original_content: DataFrame) -> DataFrame:
    return with_original_content.withWatermark("created_at", "1 second")
