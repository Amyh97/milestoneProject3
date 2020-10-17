import os
from flask import Flask
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'task_manager'
MONGO_URI = os.environ.get("MONGO_URI")
mongo = PyMongo(app)
