from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def Script_1(spark: SparkSession, bot_messages: DataFrame) -> DataFrame:
    out0 = bot_messages.withColumn(
        'value_parsed',
        from_json(
          col('value'),
          StructType([
                    StructField('channel', StringType()),
                    StructField('ts', StringType()),
                    StructField('text', StringType()),
                    StructField('source', StringType())

        ])
        )
    )

    return out0
