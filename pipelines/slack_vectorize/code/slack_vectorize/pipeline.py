from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from slack_vectorize.config.ConfigStore import *
from slack_vectorize.udfs.UDFs import *
from prophecy.utils import *
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_vectorize.graph import *

def pipeline(spark: SparkSession) -> None:
    df_slack_bronze_conversations = slack_bronze_conversations(spark)
    df_unique_only = unique_only(spark, df_slack_bronze_conversations)
    df_add_threads = add_threads(spark, df_unique_only, df_unique_only)
    df_clean = clean(spark, df_add_threads)
    df_group_threads = group_threads(spark, df_clean)
    df_merge_msgs = merge_msgs(spark, df_group_threads)
    df_vectorize = vectorize(spark, df_merge_msgs)
    df_rename = rename(spark, df_vectorize)
    slack_silver_conversations_vectorized(spark, df_rename)
    df_slack_silver_conversations_vectorized_1 = slack_silver_conversations_vectorized_1(spark)
    df_prepare = prepare(spark, df_slack_silver_conversations_vectorized_1)
    df_short_threads_only = short_threads_only(spark, df_prepare)
    df_in_100_parts = in_100_parts(spark, df_short_threads_only)
    all_vectors_silver(spark, df_in_100_parts)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/slack_vectorize")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/slack_vectorize")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
