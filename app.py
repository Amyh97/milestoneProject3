#!/usr/bin/python

import os
from flask import Flask, render_template, redirect, request
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'milestoneProject'
MONGO_URI = os.environ.get("MONGO_URI")
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
recipes = mongo.db.recipes


@app.route('/')
@app.route('/browse_recipes')
def browse_recipes():
    return render_template("browse.html", rec=mongo.db.recipes.find())


@app.route('/search_recipes/', methods=["POST", "GET"])
def search_recipes():
    cuisine = request.form.get('cuisine')
    protein = request.form.get('protein')
    carbs = request.form.get('carbs')
    diet = request.form.get('diet')
    allergies = request.form.get('allergies')
    return render_template('search.html', recipes=mongo.db.recipes.find({
                            'cuisine': cuisine, 'protein': protein,
                            'carbs': carbs, 'diet': diet,
                            'allergies': allergies}))


@app.route('/search_italian')
def search_italian():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'cuisine':'italian'}))


@app.route('/search_rice')
def search_rice():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'carbs':'rice'}))


@app.route('/search_vegetarian')
def search_pasta():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'diet':'vegetarian'}))

@app.route('/search_pasta')
def search_vegetarian():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'carbs':'pasta'}))


@app.route('/search_med')
def search_med():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine':'mediterranean'}))


@app.route('/search_beef')
def search_beef():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein':'beef'}))


@app.route('/search_poultry')
def search_poultry():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein':'poultry'}))


@app.route('/search_lactose')
def search_lactose():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'diet':'lactose free'}))


@app.route('/search_mexican')
def search_mexican():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine':'mexican'}))


@app.route('/search_pork')
def search_pork():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'protein':'pork'}))


@app.route('/add_recipe', methods=["POST", "GET"])
def add_recipe():
    return "hello world"


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')),
            debug=True)
