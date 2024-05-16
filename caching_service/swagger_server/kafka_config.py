import time
import json
import os
from kafka import KafkaProducer



CELLPHONES_SERVICE_URL = os.getenv('CELLPHONES_SERVICE_URL', 'http://cellphones_service:5000')
FPT_SERVICE_URL = os.getenv('FPT_SERVICE_URL', 'http://fpt_service:5000')
GEARVN_SERVICE_URL = os.getenv('GEARVN_SERVICE_URL', 'http://gearvn_service:5000')


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