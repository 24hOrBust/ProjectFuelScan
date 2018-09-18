"""
Initialize and configure global objects
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from .utils import load_config_from_env

app = Flask(__name__)
load_config_from_env(app)

db = MongoEngine(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from .routes import *
from .hooks import *