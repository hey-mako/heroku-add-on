"""Entry point for the application."""
import os

from json import load

from flask import Flask
from pymongo import MongoClient


application = Flask(__name__)

with application.open_instance_resource('addon-manifest.json') as f:
    manifest = load(f)
    application.config['KENSA_ID'] = manifest['id']
    application.config['KENSA_PASSWORD'] = manifest['api']['password']


client = MongoClient(os.getenv('MONGO_CLIENT_URI'))
database = client.heroku

import src.views # pylint: disable=wrong-import-position
