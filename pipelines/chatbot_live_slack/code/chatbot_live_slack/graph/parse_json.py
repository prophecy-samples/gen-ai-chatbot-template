from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live_slack.config.ConfigStore import *
from chatbot_live_slack.udfs.UDFs import *

def parse_json(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        from_json(
            col("event"), 
            "struct<envelope_id:string,payload:struct<event:struct<text:string,ts:string,user:string,channel:string>>,type:string>"
          )\
          .alias("value_parsed")
    )
