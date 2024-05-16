import time
import json
import os
from kafka import KafkaProducer


TOPIC_PROCESS_NAME = "process-topic"
KAFKA_SERVER = 'kafka:9092'


producer = None
while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
    except Exception:
        print("Reconnect to Kafka server. Try again after 10s...")
        time.sleep(10)