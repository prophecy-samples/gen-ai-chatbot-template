from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def content_vectors_read(spark: SparkSession) -> DataFrame:
    return spark.read.table(f"gen_ai.web_silver.content_vectorized")
