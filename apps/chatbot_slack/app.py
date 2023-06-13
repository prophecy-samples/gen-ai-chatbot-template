import os
import sys
import json
import threading

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException

load_dotenv()

kafka_props = {
    "bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP_SERVERS"),
    "security.protocol": os.environ.get("KAFKA_SECURITY_PROTOCOL"),
    "sasl.mechanisms": os.environ.get("KAFKA_SASL_MECHANISM"),
    "sasl.username": os.environ.get("KAFKA_SASL_USERNAME"),
    "sasl.password": os.environ.get("KAFKA_SASL_PASSWORD")
}

kafka_props_producer = kafka_props.copy()
kafka_props_consumer = kafka_props.copy()
kafka_props_consumer["group.id"] = "gen-ai-chatbot"
kafka_props_consumer["group.id"] = "latest"
kafka_props_consumer["session.timeout.ms"] = os.environ.get("KAFKA_SESSION_TIMEOUT")

producer = Producer(kafka_props)


def background_consumer(kafka_props_consumer):
    consumer = Consumer(kafka_props_consumer)

    try:
        consumer.subscribe(["knowledge-bot-messages"])

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write("%% %s [%d] reached end at offset %d\n" %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())

            print(msg.key(), "; ", msg.value())
            parsed = json.loads(msg.value())
            if parsed["source"] == "chatbot":
                app.client.chat_postMessage(
                    channel=parsed["channel"],
                    text=parsed["answer"]
                )
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.event("message")
def handle_message_events(message, say):
    channel = message["channel"]
    ts = message["ts"]
    text = message["text"]

    key = f"{channel}-{ts}-user"
    value = {
        "channel": channel,
        "ts": ts,
        "text": text,
        "source": "user"
    }

    print("Sending: ", key, "; ", value)
    producer.produce("knowledge-bot-messages", key=key, value=json.dumps(value))


# Start your app
if __name__ == "__main__":
    t = threading.Thread(target=background_consumer, args=(kafka_props_consumer,))
    t.start()

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
