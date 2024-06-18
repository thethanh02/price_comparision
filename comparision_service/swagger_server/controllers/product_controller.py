import connexion
import six
import requests
import os
import uuid
import json
from flask import Response
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server import util
from swagger_server.cache_config import cache
from swagger_server.kafka_config import producer, TOPIC_PROCESS_NAME
from flask_cors import cross_origin
from kafka import KafkaConsumer


CACHING_SERVICE_URL = os.getenv('CACHING_SERVICE_URL', 'http://caching_service:5000')
TOPIC_PROCESS_NAME = "process-topic"
KAFKA_SERVER = 'kafka:9092'
CONSUMER_GROUP_PROCESS = "process-consumers"
CELLPHONES_SERVICE_URL = os.getenv('CELLPHONES_SERVICE_URL', 'http://cellphones_service:5000')
FPT_SERVICE_URL = os.getenv('FPT_SERVICE_URL', 'http://fpt_service:5000')
GEARVN_SERVICE_URL = os.getenv('GEARVN_SERVICE_URL', 'http://gearvn_service:5000')

@cross_origin()
def api_product_get(name):  # noqa: E501
    """api_product_get

    Returns products # noqa: E501

    :param name: product name
    :type name: str

    :rtype: ApiResponse
    """
    data = cache.get(name)
    if data:
        producer.send(
            TOPIC_PROCESS_NAME,
            value={
                'call_from': 'REDIS',
                'message': None,
            }
        )
        response = {
            'total': len(data),
            'data': data,
            'cached': True
        }
    else:
        total = 0
        products = []

        producer.send(
            TOPIC_PROCESS_NAME,
            value={
                'call_from': 'CELLPHONES',
                'message': 'Bắt đầu lấy dữ liệu từ Cellphones',
            }
        )
        response_cell = requests.get(f'{CELLPHONES_SERVICE_URL}/api/product?name={name}')
        if response_cell.status_code == 200:
            producer.send(
                TOPIC_PROCESS_NAME,
                value={
                    'call_from': 'CELLPHONES',
                    'message': 'Lấy dữ liệu từ CellphoneS thành công',
                }
            )
            product_cell = response_cell.json()
            total += product_cell['total']
            products += product_cell['data']
        else:
            producer.send(
                TOPIC_PROCESS_NAME,
                value={
                    'call_from': 'CELLPHONES',
                    'message': 'Lấy dữ liệu từ CellphoneS thất bại',
                }
            )

        producer.send(
            TOPIC_PROCESS_NAME,
            value={
                'call_from': 'FPT',
                'message': 'Bắt đầu lấy dữ liệu từ Fpt',
            }
        )
        response_fpt = requests.get(f'{FPT_SERVICE_URL}/api/product?name={name}')
        if response_fpt.status_code == 200:
            producer.send(
                TOPIC_PROCESS_NAME,
                value={
                    'call_from': 'FPT',
                    'message': 'Lấy dữ liệu từ Fpt thành công',
                }
            )
            product_cell = response_fpt.json()
            total += product_cell['total']
            products += product_cell['data']
        else:
            producer.send(
                TOPIC_PROCESS_NAME,
                value={
                    'call_from': 'FPT',
                    'message': 'Lấy dữ liệu từ Fpt thành công',
                }
            )

        producer.send(
            TOPIC_PROCESS_NAME,
            value={
                'call_from': 'GEARVN',
                'message': 'Bắt đầu lấy dữ liệu từ GearVn'
            }
        )
        response_gear = requests.get(f'{GEARVN_SERVICE_URL}/api/product?name={name}')
        if response_gear.status_code == 200:
            producer.send(
                TOPIC_PROCESS_NAME,
                value={
                    'call_from': 'FPT',
                    'message': 'Lấy dữ liệu từ Fpt thành công',
                }
            )
            product_cell = response_gear.json()
            total += product_cell['total']
            products += product_cell['data']
        else:
            producer.send(
                TOPIC_PROCESS_NAME,
                value={
                    'call_from': 'FPT',
                    'message': 'Lấy dữ liệu từ Fpt thất bại',
                }
            )

        response = {
            'total': total,
            'data': products,
            'cached': False
        }

    products = response['data']

    producer.send(
        TOPIC_PROCESS_NAME,
        value={
            'call_from': 'comparision',
            'message': 'Đang so sánh giá',
        }
    )

    sorted_data = sorted(products, key=lambda element: element['price'], reverse=True)
    cache.set(name, sorted_data)
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
