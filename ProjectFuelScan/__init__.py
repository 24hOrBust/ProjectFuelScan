"""
Initialize and configure global objects
"""

from flask import Flask
from flask_mongoengine import MongoEngine
from .utils import load_config_from_env

app = Flask(__name__)
load_config_from_env(app)

db = MongoEngine(app)

from .routes import *