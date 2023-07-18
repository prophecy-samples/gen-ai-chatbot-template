from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def parse_json(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        from_json(
            col("event"), 
            "struct<envelope_id:string,payload:struct<event:struct<text:string,ts:string,user:string,channel:string>>,type:string>"
          )\
          .alias("value_parsed")
    )
