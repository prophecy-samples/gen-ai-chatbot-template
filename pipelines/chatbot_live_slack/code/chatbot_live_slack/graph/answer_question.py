from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live_slack.config.ConfigStore import *
from chatbot_live_slack.udfs.UDFs import *

def answer_question(spark: SparkSession, Aggregate_1: DataFrame) -> DataFrame:
    from spark_ai.llms.openai import OpenAiLLM
    from pyspark.dbutils import DBUtils
    OpenAiLLM(api_key = DBUtils(spark).secrets.get(scope = "open_ai", key = "token")).register_udfs(spark = spark)

    return Aggregate_1\
        .withColumn("_context", col("content_chunk"))\
        .withColumn("_query", col("input"))\
        .withColumn(
          "openai_answer",
          expr(
            "openai_answer_question(_context, _query, \" Answer the question based on the context below. Formulate the answer as if you were Shakespeare writing one of his plays! Reformulate any words that Shakespeare wouldn't know into explanations that he would understand. \n\nContext:\n```\n{context}\n```\n\nQuestion: \n```\n{query}\n```\n\nAnswer:\n \")"
          )
        )\
        .drop("_context", "_query")
