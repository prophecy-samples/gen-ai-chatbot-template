from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *
from prophecy.utils import *
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_vectorize.graph import *

def pipeline(spark: SparkSession) -> None:
    df_web_bronze_content = web_bronze_content(spark)
    df_chunkify = chunkify(spark, df_web_bronze_content)
    df_FlattenSchema_1 = FlattenSchema_1(spark, df_chunkify)
    df_with_id = with_id(spark, df_FlattenSchema_1)
    df_vectorize = vectorize(spark, df_with_id)
    df_filter_out_errors = filter_out_errors(spark, df_vectorize)
    df_rename = rename(spark, df_filter_out_errors)
    web_silver_content_vectorized(spark, df_rename)
    df_web_silver_content_vectorized_read = web_silver_content_vectorized_read(spark)
    all_vectors_silver(spark, df_web_silver_content_vectorized_read)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/web_vectorize")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/web_vectorize")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
