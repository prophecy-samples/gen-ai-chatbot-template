from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def flatten_content(spark: SparkSession, TextProcessing_1: DataFrame) -> DataFrame:
    flt_col = TextProcessing_1.withColumn("result_chunks", explode_outer("result_chunks")).columns
    selectCols = [col("url") if "url" in flt_col else col("url"),                   col("content_chunk") if "content_chunk" in flt_col else col("result_chunks").alias("content_chunk")]

    return TextProcessing_1.withColumn("result_chunks", explode_outer("result_chunks")).select(*selectCols)
