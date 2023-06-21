from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from chatbot_live_slack.config.ConfigStore import *
from chatbot_live_slack.udfs.UDFs import *
from prophecy.utils import *
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live_slack.graph import *

def pipeline(spark: SparkSession) -> None:
    df_slack_chat = slack_chat(spark)
    df_parse_json = parse_json(spark, df_slack_chat)
    df_only_user_msgs = only_user_msgs(spark, df_parse_json)
    df_extract_fields = extract_fields(spark, df_only_user_msgs)
    df_vectorize_question = vectorize_question(spark, df_extract_fields)
    df_web_silver_content_vectorized = web_silver_content_vectorized(spark)
    df_vector_lookup = vector_lookup(spark, df_vectorize_question)
    df_explode_matches = explode_matches(spark, df_vector_lookup)
    df_with_original_content = with_original_content(spark, df_explode_matches, df_web_silver_content_vectorized)
    df_with_watermark = with_watermark(spark, df_with_original_content)
    df_collect_results = collect_results(spark, df_with_watermark)
    df_answer_question = answer_question(spark, df_collect_results)
    df_prepare_payload = prepare_payload(spark, df_answer_question)
    bot_messages_target(spark, df_prepare_payload)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/chatbot_live_slack")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/chatbot_live_slack")
    pipeline(spark)
    
    spark.streams.resetTerminated()
    spark.streams.awaitAnyTermination()
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
