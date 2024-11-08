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
def landing_page():
    return render_template('landing_page.html')

@app.route('/make_account', methods=['GET'])
def make_account():
    return render_template('user_login.html', create_account=True)

@app.route('/login', methods=['GET'])
def input_login():
    return render_template('user_login.html', create_account=False)

# actually adding the account
@app.route('/manage_account', methods=['GET'])
def manage_account():
    create_login = flask.request.args.get('create')

    if create_login == 'false': 
        username = flask.request.args.get('username')
        password = flask.request.args.get('password')
    else: 
        username = flask.request.args.get('new_username')
        password = flask.request.args.get('new_password')

    print("USERNAME", username)
    print("PASSWORD", password)
    print("GETUSER", db.get_user(username))
    print("VALID", db.user_login_valid(username, password)) # why is INTS not working??
    print("TEST", db.user_login_valid('kx', 11))

    if create_login == 'false':
        if db.user_login_valid(username, password) not in ["Password incorrect", "EmailId not found"]:
            return pantry_page()
        else:
            # force them to retype if user is wrong
            return input_login()
    else:
        # if we did create a login, we add the user
        db.insert_user(username, password)
        return landing_page()

@app.route('/pantry', methods=['GET'])
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









