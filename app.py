import os
from flask import Flask, render_template, redirect
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'task_manager'
MONGO_URI = os.environ.get("MONGO_URI")
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)


@app.route('/')
@app.route('/browse_recipes')
def browse_recipes():
    return render_template('browse.html', recipes=mongo.db.recipes.find())
