import connexion
import six
import requests
import os
import uuid
import json
from flask import Response
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server import util
from swagger_server.kafka_config import producer, TOPIC_PROCESS_NAME
from flask_cors import cross_origin
from kafka import KafkaConsumer


CACHING_SERVICE_URL = os.getenv('CACHING_SERVICE_URL', 'http://caching_service:5000')
TOPIC_PROCESS_NAME = "process-topic"
KAFKA_SERVER = 'kafka:9092'
CONSUMER_GROUP_PROCESS = "process-consumers"


@cross_origin()
def api_product_get(name):  # noqa: E501
    """api_product_get

    Returns products # noqa: E501

    :param name: product name
    :type name: str

    :rtype: ApiResponse
    """
    # product = Product.from_dict()
    response = requests.get(f'{CACHING_SERVICE_URL}/api/product?name={name}').json()
    products = response['data']

    producer.send(
        TOPIC_PROCESS_NAME,
        value={
            'call_from': 'comparision',
            'message': 'Đang so sánh giá',
        }
    )

    sorted_data = sorted(products, key=lambda element: element['price'], reverse=True)
    producer.send(
        TOPIC_PROCESS_NAME,
        value={
            'call_from': 'comparision',
            'message': 'Đang xử lý dữ liệu',
        }
    )
    handled_products = [{
        'id': uuid.uuid4(),
        'name': product['name'], 
        'price_numberic': product['price'],
        'price': '{:0,.0f}'.format(product['price']).replace(",", ".") + " đ",
        'image': product['image'],
        'url': product['url'],
        'website': product['website']
    } for product in sorted_data]
    response['data'] = handled_products

    producer.send(
        TOPIC_PROCESS_NAME,
        value={
            'call_from': 'comparision',
            'message': None, # done
        }
    )
    return response


def stream_get():  # noqa: E501
    """stream_get

    Returns message stream # noqa: E501


    :rtype: str
    """
    consumer_process = KafkaConsumer(
        client_id="clientProcess",
        group_id=CONSUMER_GROUP_PROCESS,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode('ascii')),
        key_deserializer=lambda v: json.loads(v.decode('ascii')),
        max_poll_records=10,
        auto_offset_reset='earliest',
        session_timeout_ms=6000,
        heartbeat_interval_ms=3000
    )
    consumer_process.subscribe(topics=[TOPIC_PROCESS_NAME])
    def get_data():
        for message in consumer_process:
            yield f'data: {message.value["message"] or ""} \n\n'
    return Response(get_data(), mimetype='text/event-stream')
