from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from web_ingest.config.ConfigStore import *
from web_ingest.udfs.UDFs import *
from prophecy.utils import *
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_ingest.graph import *

def pipeline(spark: SparkSession) -> None:
    df_web_bronze_url = web_bronze_url(spark)
    df_text_only = text_only(spark, df_web_bronze_url)
    web_bronze_sitemap_raw(spark, df_text_only)
    df_web_bronze_sitemap = web_bronze_sitemap(spark)
    df_scrape_pages = scrape_pages(spark, df_web_bronze_sitemap)
    web_bronze_content_1(spark, df_scrape_pages)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/web_ingest")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/web_ingest")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
