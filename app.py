#!/usr/bin/python

import os
from flask import Flask, render_template, request, redirect, url_for, flash
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
app.config.update(SECRET_KEY=os.urandom(24))


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
    heading = "Italian Dishes"
    italian = mongo.db.recipes.find({'cuisine': 'italian'})
    return render_template('results.html', recipes=italian, heading=heading)


@app.route('/search_rice', methods=['GET'])
def search_rice():
    heading = "Rice Dishes"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'carbs': 'rice'}), heading=heading)


@app.route('/search_vegetarian', methods=['GET'])
def search_vegetarian():
    heading = "Vegetarian Dishes"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'diet': 'vegetarian'}), heading=heading)


@app.route('/search_pasta', methods=['GET'])
def search_pasta():
    heading = "Pasta Dishes"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'carbs': 'pasta'}), heading=heading)


@app.route('/search_sweet', methods=['GET'])
def search_sweet():
    heading = "Sweet Treats"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine': 'sweet'}), heading=heading)


@app.route('/search_beef', methods=['GET'])
def search_beef():
    heading = "Beef Dishes"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein': 'beef'}), heading=heading)


@app.route('/search_poultry', methods=['GET'])
def search_poultry():
    heading = "Poultry Dishes"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein': 'poultry'}), heading=heading)


@app.route('/search_mexican', methods=['GET'])
def search_mexican():
    heading = "Mexican Dishes"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine': 'mexican'}), heading=heading)


@app.route('/search_pork', methods=['GET'])
def search_pork():
    heading = "Pork Dishes"
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'protein': 'pork'}), heading=heading)


# add recipe
@app.route('/recipe/add', methods=['POST', 'GET'])
def add_recipe():
    if request.method == "POST":
        flash("Thank you, this recipe has been added.")
        new_recipe = {
            "name": request.form.get("name"),
            "cuisine": request.form.getlist("cuisine"),
            "protein": request.form.getlist("protein"),
            "carbs": request.form.getlist("carbs"),
            "diet": request.form.getlist("diet"),
            "allergies": request.form.getlist("allergies"),
            "ingredients": request.form.get("ingredients"),
            "method": request.form.get("method"),
            "notes": request.form.get("notes"),
            "image": request.form.get("image"),
            "source": request.form.get("source")
        }
        mongo.db.recipes.insert_one(new_recipe)
        return redirect(url_for('recipes',
                        cuisine=mongo.db.cuisine.find(),
                        protein=mongo.db.protein.find(),
                        carbs=mongo.db.carbs.find(),
                        diet=mongo.db.diet.find(),
                        allergies=mongo.db.allergies.find()))
    else:
        return render_template('add.html',
                               cuisine=mongo.db.cuisine.find(),
                               protein=mongo.db.protein.find(),
                               carbs=mongo.db.carbs.find(),
                               diet=mongo.db.diet.find(),
                               allergies=mongo.db.allergies.find())


# recipe edit
@app.route('/recipe/<recipe_id>/edit', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if request.method == 'POST':
        flash("Thank you, this recipe has been updated.")
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
            'image': request.form.get('image'),
            'source': request.form.get('source')
          })
        return redirect(url_for('recipes',
                                recipes=recipes,
                                cuisine=list(mongo.db.cuisine.find()),
                                protein=list(mongo.db.protein.find()),
                                carbs=list(mongo.db.carbs.find()),
                                diet=list(mongo.db.diet.find()),
                                allergies=list(mongo.db.allergies.find())))
    else:
        return render_template('update.html',
                               recipes=recipes,
                               cuisine=mongo.db.cuisine.find(),
                               protein=mongo.db.protein.find(),
                               carbs=mongo.db.carbs.find(),
                               diet=mongo.db.diet.find(),
                               allergies=mongo.db.allergies.find())

# delete recipe


@app.route('/recipe/<recipe_id>/delete')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipes'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),
            debug=True)
