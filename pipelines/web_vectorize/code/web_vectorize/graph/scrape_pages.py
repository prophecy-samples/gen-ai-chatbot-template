from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def scrape_pages(spark: SparkSession, web_bronze_sitemap: DataFrame) -> DataFrame:
    return web_bronze_sitemap.select(col("loc").alias("url"), scrape_text(col("loc")).alias("content"))
