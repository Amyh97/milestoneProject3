import os
from flask import Flask, render_template, redirect
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


@app.route('/')
@app.route('/browse_recipes')
def browse_recipes():
    return render_template("browse.html", recipes=mongo.db.recipes.find())

@app.route('/search_recipes')
def search_recipes():
    return render_template("search.html", recipes=mongo.db.recipes.find())

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('search_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT'
           )), debug=True)
