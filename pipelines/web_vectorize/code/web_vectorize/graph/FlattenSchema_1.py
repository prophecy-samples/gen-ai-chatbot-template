from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def FlattenSchema_1(spark: SparkSession, TextProcessing_1: DataFrame) -> DataFrame:
    return TextProcessing_1\
        .withColumn("result_chunks", explode_outer("result_chunks"))\
        .select(col("url"), col("result_chunks").alias("content_chunk"))
