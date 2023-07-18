from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def chunkify(spark: SparkSession, in0: DataFrame) -> DataFrame:
    from pyspark.sql.functions import expr, array, struct
    from spark_ai.files.text import FileTextUtils
    FileTextUtils().register_udfs(spark)

    return in0.withColumn("result_chunks", expr(f"text_split_into_chunks(content, 1000)"))
