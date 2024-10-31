import flask
from flask import Flask, render_template
import DatabaseClient
import pandas as pd
import numpy as np
import json
from urllib.parse import unquote

app = Flask(__name__)
db = DatabaseClient.DatabaseClient()

@app.route('/', methods=['GET'])
@app.route('/?', methods=['GET'])
@app.route('/index', methods=['GET'])
def pantry_page():
    ingredients = pd.read_csv('webscraping/output/ingredients_list.csv')
    ingredients = ingredients.values.tolist()
    ingredients = np.squeeze(ingredients)
    return render_template('prototype_pantry.html', ingredients=ingredients)

@app.route('/recommended_recipes', methods=['GET'])
def results_page():
    ingredient_list = flask.request.args.get("ingredients")
    ingredient_list = json.loads(ingredient_list) 
    ingredient_list = [ingredient.lower() for ingredient in ingredient_list]
    recipes = db.get_recipes_ingredients(ingredient_list)
    
    return render_template('prototype_recommended_recipes.html', recipes=recipes)

@app.route('/all_recipes', methods=['GET'])
def all_recipes():
    #flask.request.args(ingredient_list)
    recipes = db.get_all_recipes()
    return render_template('prototype_recommended_recipes.html', recipes=recipes)

@app.route('/recipe_page', methods=['GET'])
def recipe_page():
    # blah
    recipe_id = flask.request.args.get("recipe")
    
    #recipe_title = unquote(recipe_title)
    # get recipe with recipe title
    recipe = db.return_recipe(recipe_id)
    return render_template('prototype_recipe_page.html', recipe=recipe)







