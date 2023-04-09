#!/bin/env python3
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# configure Flask app
import config

# Init DB and declare all db models
from models import *

# Setup flask security
import auth

import api

from worker import celery

import jobs

import sse

from cache import cache

if __name__ == '__main__':
    app.run()
