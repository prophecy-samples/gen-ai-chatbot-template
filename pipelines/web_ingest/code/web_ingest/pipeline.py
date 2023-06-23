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
    df_index_web_read = index_web_read(spark)
    df_text_only = text_only(spark, df_index_web_read)
    index_web_text(spark, df_text_only)
    df_index_urls = index_urls(spark)
    df_scrape_pages = scrape_pages(spark, df_index_urls)
    df_clean_fields = clean_fields(spark, df_scrape_pages)
    web_content(spark, df_clean_fields)

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
