from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def all_vectors_silver(spark: SparkSession, web_silver_content_vectorized_1: DataFrame):
    from pyspark.sql.functions import expr, array, struct
    from spark_ai.dbs.pinecone import PineconeDB, IdVector
    from pyspark.dbutils import DBUtils
    PineconeDB(DBUtils(spark).secrets.get(scope = "pinecone", key = "token"), "us-east-1-aws").register_udfs(spark)

    if spark.catalog.tableExists(f"prophecy_data.operational.pinecone_vectors_upsert_status"):
        web_silver_content_vectorized_1\
            .withColumn("id_vectors", array(struct(col("id"), col("embedding").alias("vector"))))\
            .withColumn("upserted", expr(f"pinecone_upsert(\"all-vectors\", id_vectors)"))\
            .select(col("*"), col("upserted.*"))\
            .select(col("id_vectors"), col("count"), col("error"))\
            .write\
            .format("delta")\
            .insertInto(f"prophecy_data.operational.pinecone_vectors_upsert_status")
    else:
        web_silver_content_vectorized_1\
            .withColumn("id_vectors", array(struct(col("id"), col("embedding").alias("vector"))))\
            .withColumn("upserted", expr(f"pinecone_upsert(\"all-vectors\", id_vectors)"))\
            .select(col("*"), col("upserted.*"))\
            .select(col("id_vectors"), col("count"), col("error"))\
            .write\
            .format("delta")\
            .mode("overwrite")\
            .saveAsTable(f"prophecy_data.operational.pinecone_vectors_upsert_status")
