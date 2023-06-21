from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from slack_ingest.config.ConfigStore import *
from slack_ingest.udfs.UDFs import *
from prophecy.utils import *
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_ingest.graph import *

def pipeline(spark: SparkSession) -> None:
    df_slack_bronze_channels_web = slack_bronze_channels_web(spark)
    slack_bronze_channels(spark, df_slack_bronze_channels_web)
    df_slack_bronze_conversations_web = slack_bronze_conversations_web(spark)
    slack_bronze_conversations(spark, df_slack_bronze_conversations_web)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/slack_ingest")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/slack_ingest")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
