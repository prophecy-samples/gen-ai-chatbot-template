from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def explode_matches(spark: SparkSession, PineconeLookup_1: DataFrame) -> DataFrame:
    return PineconeLookup_1\
        .withColumn("pinecone_matches", explode_outer("pinecone_matches"))\
        .select(col("pinecone_matches"), col("value_parsed.text").alias("input"), col("value_parsed.channel").alias("channel"), col("value_parsed.ts").alias("ts"))
