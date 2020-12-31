#!/usr/bin/python

import os
from flask import Flask, render_template, request
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if path.exists('env.py'):
    import env


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'milestoneProject'
MONGO_URI = os.environ.get('MONGO_URI')
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
recipes = mongo.db.recipes


@app.route('/')
def browse_recipes():
    carousel = mongo.db.recipes.find()
    recipe = (list(carousel)[-5:])
    one = recipe[0]
    two = recipe[1]
    three = recipe[2]
    four = recipe[3]
    five = recipe[4]
    return render_template('browse.html', one=one,
                           two=two, three=three, four=four, five=five)


# search recipe
@app.route('/recipes', methods=["POST", "GET"])
def recipes():
    query_object = {}
    cuisine = request.form.getlist('cuisine')
    protein = request.form.getlist('protein')
    carbs = request.form.getlist('carbs')
    diet = request.form.getlist('diet')
    if cuisine:
        query_object['cuisine'] = {'$in': cuisine}
    if protein:
        query_object['protein'] = {'$in': protein}
    if carbs:
        query_object['carbs'] = {'$in': carbs}
    if diet:
        query_object['diet'] = {'$in': diet}
    recipes = mongo.db.recipes.find(query_object)
    return render_template('search.html', recipes=recipes,
                           cuisine=mongo.db.cuisine.find(),
                           protein=mongo.db.protein.find(),
                           carbs=mongo.db.carbs.find(),
                           diet=mongo.db.diet.find())


""" methods for browse page to sort by 1 thing
in browse.html and opens results.html """


@app.route('/search_italian', methods=['GET'])
def search_italian():
    italian = mongo.db.recipes.find({'cuisine': 'italian'})
    return render_template('results.html', recipes=italian)


@app.route('/search_rice', methods=['GET'])
def search_rice():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'carbs': 'rice'}))


@app.route('/search_vegetarian', methods=['GET'])
def search_vegetarian():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'diet': 'vegetarian'}))


@app.route('/search_pasta', methods=['GET'])
def search_pasta():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'carbs': 'pasta'}))


@app.route('/search_sweet', methods=['GET'])
def search_sweet():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine': 'sweet'}))


@app.route('/search_beef', methods=['GET'])
def search_beef():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein': 'beef'}))


@app.route('/search_poultry', methods=['GET'])
def search_poultry():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein': 'poultry'}))


@app.route('/search_lactose', methods=['GET'])
def search_lactose():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'diet': 'lactose free'}))


@app.route('/search_mexican', methods=['GET'])
def search_mexican():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine': 'mexican'}))


@app.route('/search_pork', methods=['GET'])
def search_pork():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'protein': 'pork'}))


# add recipe
@app.route('/recipe/add', methods=['POST', 'GET'])
def add_recipe():
    if request.method == "POST":
        new_recipe = {
            "name": request.form.get("name"),
            "cuisine": request.form.getlist("cuisine"),
            "protein": request.form.getlist("protein"),
            "carbs": request.form.getlist("carbs"),
            "diet": request.form.getlist("diet"),
            "allergies": request.form.getlist("allergies"),
            "ingredients": request.form.getlist("ingredients"),
            "method": request.form.get("method"),
            "notes": request.form.get("notes"),
            "image": request.form.get("image")
        }
        mongo.db.recipes.insert_one(new_recipe)
    return render_template(
        "add.html",
        cuisine=mongo.db.cuisine.find(),
        protein=mongo.db.protein.find(),
        carbs=mongo.db.carbs.find(),
        diet=mongo.db.diet.find(),
        allergies=mongo.db.allergies.find(),
    )


""" update recipes page
not pre-checking checkboxes so being updated with empty values
"""


# recipe edit
@app.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes.find({"id_": ObjectId(recipe_id)})
    if request.method == 'POST':
        mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, {
            'name': request.form.get('name'),
            'cuisine': request.form.getlist('cuisine'),
            'protein': request.form.getlist('protein'),
            'carbs': request.form.getlist('carbs'),
            'diet': request.form.getlist('diet'),
            'allergies': request.form.getlist('allergies'),
            'ingredients': request.form.get('ingredients'),
            'method': request.form.get('method'),
            'notes': request.form.get('notes'),
            'image': request.form.get('image')
          })
    return render_template('update.html',
                           recipes=recipes,
                           cuisine=mongo.db.cuisine.find(),
                           protein=mongo.db.protein.find(),
                           carbs=mongo.db.carbs.find(),
                           diet=mongo.db.diet.find(),
                           allergies=mongo.db.allergies.find()
                           )

# delete recipe


@app.route('/recipe/<recipe_id>/delete')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),
            debug=True)
