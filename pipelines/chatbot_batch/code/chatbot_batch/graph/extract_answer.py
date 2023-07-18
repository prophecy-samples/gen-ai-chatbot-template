from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_batch.config.ConfigStore import *
from chatbot_batch.udfs.UDFs import *

def extract_answer(spark: SparkSession, answer_question: DataFrame) -> DataFrame:
    return answer_question.select(col("openai_answer.choices")[0].alias("answer"))
