from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from chatbot_batch.config.ConfigStore import *
from chatbot_batch.udfs.UDFs import *
from prophecy.utils import *
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_batch.graph import *

def pipeline(spark: SparkSession) -> None:
    df_question_seed = question_seed(spark)
    df_vectorize_question = vectorize_question(spark, df_question_seed)

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
