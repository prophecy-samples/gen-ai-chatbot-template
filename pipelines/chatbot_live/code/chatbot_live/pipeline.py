from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *
from prophecy.utils import *
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.graph import *

def pipeline(spark: SparkSession) -> None:
    df_bot_messages = bot_messages(spark)
    df_parse_json = parse_json(spark, df_bot_messages)
    df_only_user_msgs = only_user_msgs(spark, df_parse_json)
    df_web_silver_content_vectorized = web_silver_content_vectorized(spark)
    df_vectorize_question = vectorize_question(spark, df_only_user_msgs)
    df_vector_lookup = vector_lookup(spark, df_vectorize_question)
    df_explode_matches = explode_matches(spark, df_vector_lookup)
    df_with_original_content = with_original_content(spark, df_explode_matches, df_web_silver_content_vectorized)
    df_answer_question = answer_question(spark, df_with_original_content)
    df_prepare_payload = prepare_payload(spark, df_answer_question)
    bot_messages_1(spark, df_prepare_payload)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/chatbot_live")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/chatbot_live")
    pipeline(spark)
    
    spark.streams.resetTerminated()
    spark.streams.awaitAnyTermination()
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
