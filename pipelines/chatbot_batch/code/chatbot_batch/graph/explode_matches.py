from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_batch.config.ConfigStore import *
from chatbot_batch.udfs.UDFs import *

def explode_matches(spark: SparkSession, PineconeLookup_1: DataFrame) -> DataFrame:
    flt_col = PineconeLookup_1.withColumn("pinecone_matches", explode_outer("pinecone_matches")).columns
    selectCols = [col("pinecone_matches") if "pinecone_matches" in flt_col else col("pinecone_matches"),                   col("input") if "input" in flt_col else col("input")]

    return PineconeLookup_1.withColumn("pinecone_matches", explode_outer("pinecone_matches")).select(*selectCols)
