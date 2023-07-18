from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *
from prophecy.utils import *
from web_vectorize.graph import *

def pipeline(spark: SparkSession) -> None:
    df_web_content = web_content(spark)
    df_chunkify = chunkify(spark, df_web_content)
    df_flatten_content = flatten_content(spark, df_chunkify)
    df_with_id = with_id(spark, df_flatten_content)
    df_vectorize = vectorize(spark, df_with_id)
    df_clean = clean(spark, df_vectorize)
    df_rename = rename(spark, df_clean)
    content_vectors(spark, df_rename)
    df_content_vectors_read = content_vectors_read(spark)
    vector_db(spark, df_content_vectors_read)

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
