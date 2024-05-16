# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Product(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, price: float=None, image: str=None, url: str=None, website: str=None):  # noqa: E501
        """Product - a model defined in Swagger

        :param name: The name of this Product.  # noqa: E501
        :type name: str
        :param price: The price of this Product.  # noqa: E501
        :type price: float
        :param image: The image of this Product.  # noqa: E501
        :type image: str
        :param url: The url of this Product.  # noqa: E501
        :type url: str
        :param website: The website of this Product.  # noqa: E501
        :type website: str
        """
        self.swagger_types = {
            'name': str,
            'price': float,
            'image': str,
            'url': str,
            'website': str
        }

        self.attribute_map = {
            'name': 'name',
            'price': 'price',
            'image': 'image',
            'url': 'url',
            'website': 'website'
        }
        self._name = name
        self._price = price
        self._image = image
        self._url = url
        self._website = website

    @classmethod
    def from_dict(cls, dikt) -> 'Product':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Product of this Product.  # noqa: E501
        :rtype: Product
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Product.


        :return: The name of this Product.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Product.


        :param name: The name of this Product.
        :type name: str
        """

        self._name = name

    @property
    def price(self) -> float:
        """Gets the price of this Product.


        :return: The price of this Product.
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price: float):
        """Sets the price of this Product.


        :param price: The price of this Product.
        :type price: float
        """

        self._price = price

    @property
    def image(self) -> str:
        """Gets the image of this Product.


        :return: The image of this Product.
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image: str):
        """Sets the image of this Product.


        :param image: The image of this Product.
        :type image: str
        """

        self._image = image

    @property
    def url(self) -> str:
        """Gets the url of this Product.


        :return: The url of this Product.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this Product.


        :param url: The url of this Product.
        :type url: str
        """

        self._url = url

    @property
    def website(self) -> str:
        """Gets the website of this Product.


        :return: The website of this Product.
        :rtype: str
        """
        return self._website

    @website.setter
    def website(self, website: str):
        """Sets the website of this Product.


        :param website: The website of this Product.
        :type website: str
        """

        self._website = website
