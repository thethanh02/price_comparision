import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.product import Product
from swagger_server import util
from swagger_server.kafka_config import producer, TOPIC_PROCESS_NAME


def api_product_get(name):  # noqa: E501
    """api_product_get

    Returns products # noqa: E501

    :param name: product name
    :type name: str

    :rtype: ApiResponse
    """
    producer.send(
        TOPIC_PROCESS_NAME,
        value={
            'call_from': 'FPT',
            'message': 'Đang lấy dữ liệu từ Fpt',
        }
    )
    products = Product.find_product(name)
    return ApiResponse.from_dict({
        'total': len(products),
        'data': products
    })
