import flask
from flask import Flask, render_template
import DatabaseClient
import pandas as pd
import numpy as np
import json
from urllib.parse import unquote
import dotenv
import auth
import os
from top import app

db = DatabaseClient.DatabaseClient()

dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route('/', methods=['GET'])
@app.route('/?', methods=['GET'])
@app.route('/index', methods=['GET'])
def landing_page():
    username = auth.authenticate()
    return render_template('landing_page.html', username=username)

'''
@app.route('/make_account', methods=['GET'])
def make_account():
    username = auth.authenticate()
    return render_template('user_login.html', username=username, create_account=True)

@app.route('/login', methods=['GET'])
def input_login():
    username = auth.authenticate()
    return render_template('user_login.html', username=username, create_account=False)

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
    
    # print("USERNAME", username)
    # print("PASSWORD", password)
    # print("GETUSER", db.get_user(username))
    # print("VALID", db.user_login_valid(username, password)) # why is INTS not working??
    # print("TEST", db.user_login_valid('kx', 11))

    if create_login == 'false':
        if db.user_login_valid(username, password) not in ["Password incorrect", "EmailId not found"]:
            response = make_response(pantry_page())
            response.set_cookie('emailId', username)
            return response
        else:
            # force them to retype if user is wrong
            return input_login()
    else:
        # if we did create a login, we add the user
        db.insert_user(username, password)
        return landing_page()
'''

@app.route('/pantry', methods=['GET'])
def pantry_page():
    username = auth.authenticate()
    ingredients = pd.read_csv('webscraping/output/ingredients_list.csv')
    ingredients = ingredients.values.tolist()
    ingredients = np.squeeze(ingredients)
    return render_template('prototype_pantry.html', ingredients=ingredients, username=username)

@app.route('/recommended_recipes', methods=['GET'])
def results_page():
    username = auth.authenticate()
    ingredient_list = flask.request.args.get("ingredients")
    ingredient_list = json.loads(ingredient_list) 
    ingredient_list = [ingredient.lower() for ingredient in ingredient_list]
    recipes = db.get_recipes_ingredients(ingredient_list)
    
    return render_template('prototype_recommended_recipes.html', recipes=recipes, username=username)

@app.route('/all_recipes', methods=['GET'])
def all_recipes():
    username = auth.authenticate()
    #flask.request.args(ingredient_list)
    recipes = db.get_all_recipes()
    return render_template('prototype_recommended_recipes.html', recipes=recipes, username=username)

@app.route('/recipe_page', methods=['GET'])
def recipe_page():
    username = auth.authenticate()
    recipe_id = flask.request.args.get("recipe")
    
    recipe = db.return_recipe(recipe_id)
    return render_template('prototype_recipe_page.html', recipe=recipe, username=username)

@app.route('/wishlist', methods=['GET'])
def wishlist_page():
    username = auth.authenticate()
    #email_id = flask.request.args.get("emailId")
    wish_list = flask.request.args.get("wishList")
    wishList = db.update_user_wishlist(username, wish_list)
    return render_template('wishlist.html', wishList=wishList, username=username)

@app.route('/profile-page', methods=['GET', 'POST'])
def profile_page():
    username = auth.authenticate()
    #email_id = flask.request.cookies.get("emailId")
    return render_template('profile_page.html', email_id=username)