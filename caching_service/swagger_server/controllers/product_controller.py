import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server import util
from swagger_server.cache_config import cache
from swagger_server.kafka_config import producer, TOPIC_PROCESS_NAME, CELLPHONES_SERVICE_URL, FPT_SERVICE_URL, GEARVN_SERVICE_URL
import requests


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
        return ApiResponse.from_dict({
            'total': len(data),
            'data': data,
            'cached': True
        })

    # # Nếu k bắt được cache thì gọi api
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

    cache.set(name, products)
    return ApiResponse.from_dict({
        'total': total,
        'data': products,
        'cached': False
    })
