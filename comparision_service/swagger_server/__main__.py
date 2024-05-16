#!/usr/bin/env python3

import connexion
import os
import json
from swagger_server import encoder
from swagger_server import kafka_config
from kafka import KafkaConsumer
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()


def main():
    producer = kafka_config.producer
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Comparision API'}, pythonic_params=True)
    cors = CORS(app.app)
    app.app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(port=int(os.getenv('PORT', 5000)))


if __name__ == '__main__':
    main()
