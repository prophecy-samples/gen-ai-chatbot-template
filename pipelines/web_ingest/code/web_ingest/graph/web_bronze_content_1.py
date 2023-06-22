from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_ingest.config.ConfigStore import *
from web_ingest.udfs.UDFs import *

def web_bronze_content_1(spark: SparkSession, scrape_pages: DataFrame):
    scrape_pages.write\
        .format("delta")\
        .option("mergeSchema", True)\
        .option("overwriteSchema", True)\
        .mode("overwrite")\
        .saveAsTable(f"prophecy_data.web_bronze.content")
