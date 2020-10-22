import os
from flask import Flask, render_template, redirect, request
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'recipes'
MONGO_URI = os.environ.get("MONGO_URI")
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
recipes = mongo.db.recipes


@app.route('/')
@app.route('/browse_recipes')
def browse_recipes():
    return render_template("browse.html")


@app.route('/search_recipes', methods=["GET"])
def search_recipes():
    return render_template('search.html')


@app.route('/add_recipe')
def add_recipe():
    return "hello world"


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
            debug=True)
