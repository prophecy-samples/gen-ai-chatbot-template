from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from slack_ingest.config.ConfigStore import *
from slack_ingest.udfs.UDFs import *

def slack_bronze_conversations(spark: SparkSession, slack_bronze_conversations_web: DataFrame):
    if spark.catalog._jcatalog.tableExists(f"prophecy_data.slack_bronze.conversations"):
        from delta.tables import DeltaTable, DeltaMergeBuilder
        DeltaTable\
            .forName(spark, f"prophecy_data.slack_bronze.conversations")\
            .alias("target")\
            .merge(
              slack_bronze_conversations_web.alias("source"),
              ((col("source.ts") == col("target.ts")) & (col("source.channel_id") == col("target.channel_id")))
            )\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
            .execute()
    else:
        slack_bronze_conversations_web.write\
            .format("delta")\
            .option("mergeSchema", True)\
            .option("overwriteSchema", False)\
            .mode("overwrite")\
            .saveAsTable(f"prophecy_data.slack_bronze.conversations")
