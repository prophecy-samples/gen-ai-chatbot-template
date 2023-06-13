from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def bot_messages_1(spark: SparkSession, answer_question: DataFrame):
    df1 = answer_question.select(
        [to_json(struct("*")).cast('string').alias("value"), col("key").cast('string').alias("key")]
    )
    writer = df1.writeStream.format("kafka").option("checkpointLocation", "dbfs:/tmp/chatbot_live_checkpoint/")
    writer = writer.outputMode("append")
    writer\
        .options(
          **{
            "kafka.sasl.jaas.config": "kafkashaded.org.apache.kafka.common.security.scram.ScramLoginModule required username=\"NV5SP3XVKYLLM3XK\" password=\"VXO76eNNxz5ETnbsST9ioaEWLtSsC64lqjMaq+ju71bA0zRd2iW1bKNDVoogmt9f\";",
            "kafka.sasl.mechanism": "PLAIN",
            "kafka.security.protocol": "SASL_SSL",
            "kafka.bootstrap.servers": "pkc-4nym6.us-east-1.aws.confluent.cloud:9092",
            "topic": "knowledge-bot-messages",
          }
        )\
        .start()
