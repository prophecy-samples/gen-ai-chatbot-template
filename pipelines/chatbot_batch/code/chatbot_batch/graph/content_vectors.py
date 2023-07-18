from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_batch.config.ConfigStore import *
from chatbot_batch.udfs.UDFs import *

def content_vectors(spark: SparkSession) -> DataFrame:
    return spark.read.table(f"gen_ai.web_silver.content_vectorized")
