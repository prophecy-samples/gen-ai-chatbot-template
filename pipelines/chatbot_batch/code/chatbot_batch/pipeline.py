from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from chatbot_batch.config.ConfigStore import *
from chatbot_batch.udfs.UDFs import *
from prophecy.utils import *
from chatbot_batch.graph import *

def pipeline(spark: SparkSession) -> None:
    df_question_seed = question_seed(spark)
    df_vectorize_question = vectorize_question(spark, df_question_seed)
    df_content_vectors = content_vectors(spark)
    df_vector_lookup = vector_lookup(spark, df_vectorize_question)
    df_explode_matches = explode_matches(spark, df_vector_lookup)
    df_with_original_content = with_original_content(spark, df_explode_matches, df_content_vectors)
    df_collect_context = collect_context(spark, df_with_original_content)
    df_answer_question = answer_question(spark, df_collect_context)
    df_extract_answer = extract_answer(spark, df_answer_question)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/chatbot_batch")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/chatbot_batch")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
