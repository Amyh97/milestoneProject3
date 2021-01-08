#!/usr/bin/python

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if path.exists("env.py"):
    import env


app = Flask(__name__)
debug = os.environ.get("DEBUG")
app.config["MONGO_DBNAME"] = "milestoneProject"
MONGO_URI = os.environ.get("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
recipes = mongo.db.recipes
app.config.update(SECRET_KEY=os.urandom(24))


@app.route("/")
def browse_recipes():
    carousel = mongo.db.recipes.find()
    recipes = list(carousel)[-5:]
    category = mongo.db.categories.find()
    return render_template("browse.html", recipes=recipes, category=category)


# search and browse
@app.route("/recipes", methods=["POST", "GET"])
def recipes():
    # create query_object so not all fields need values
    query_object = {}
    cuisine = request.form.getlist("cuisine")
    protein = request.form.getlist("protein")
    carbs = request.form.getlist("carbs")
    diet = request.form.getlist("diet")
    if cuisine:
        query_object["cuisine"] = {"$in": cuisine}
    if protein:
        query_object["protein"] = {"$in": protein}
    if carbs:
        query_object["carbs"] = {"$in": carbs}
    if diet:
        query_object["diet"] = {"$in": diet}
    recipes = mongo.db.recipes.find(query_object)
    return render_template(
        "search.html",
        recipes=recipes,
        cuisine=mongo.db.cuisine.find(),
        protein=mongo.db.protein.find(),
        carbs=mongo.db.carbs.find(),
        diet=mongo.db.diet.find(),
    )


# add recipe
@app.route("/recipe/add", methods=["POST", "GET"])
def add_recipe():
    if request.method == "POST":
        # let users know submit was successful
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
            "source": request.form.get("source"),
        }
        mongo.db.recipes.insert_one(new_recipe)
        return redirect(url_for("recipes"))
    else:
        # renders page before form is submitted
        return render_template(
            "add.html",
            cuisine=mongo.db.cuisine.find(),
            protein=mongo.db.protein.find(),
            carbs=mongo.db.carbs.find(),
            diet=mongo.db.diet.find(),
            allergies=mongo.db.allergies.find(),
        )


# recipe edit
@app.route("/recipe/<recipe_id>/edit", methods=["GET", "POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if request.method == "POST":
        # lets users know update was successful
        flash("Thank you, this recipe has been updated.")
        mongo.db.recipes.update(
            {"_id": ObjectId(recipe_id)},
            {
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
                "source": request.form.get("source"),
            },
        )
        return redirect(
            url_for(
                "recipes",
                recipes=recipes,
                cuisine=list(mongo.db.cuisine.find()),
                protein=list(mongo.db.protein.find()),
                carbs=list(mongo.db.carbs.find()),
                diet=list(mongo.db.diet.find()),
                allergies=list(mongo.db.allergies.find()),
            )
        )
    else:
        # prevents redirect before changes are made
        return render_template(
            "update.html",
            recipes=recipes,
            cuisine=mongo.db.cuisine.find(),
            protein=mongo.db.protein.find(),
            carbs=mongo.db.carbs.find(),
            diet=mongo.db.diet.find(),
            allergies=mongo.db.allergies.find(),
        )


# delete recipe
@app.route("/recipe/<recipe_id>/delete")
def delete_recipe(recipe_id):
    # lets users know function was successful
    flash("Thank you, this recipe has been deleted.")
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for("recipes"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")))
