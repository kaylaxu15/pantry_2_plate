import flask
from flask import Flask, render_template, session, jsonify
import DatabaseClient
import pandas as pd
import numpy as np
import json
from urllib.parse import unquote
import dotenv
import auth
import os
from top import app
import cloudinary
import cloudinary.uploader

db = DatabaseClient.DatabaseClient()

dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

cloudinary.config( 
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.getenv('CLOUDINARY_API_KEY'), 
    api_secret = os.getenv('CLOUDINARY_API_SECRET'), 
    secure=True
)

@app.route('/', methods=['GET'])
@app.route('/?', methods=['GET'])
@app.route('/index', methods=['GET'])
def landing_page():
    username = auth.authenticate()
    return render_template('landing_page.html', username=username)

@app.route('/add/<item>')
def add_item(item):
    if 'items' not in session:
        session['items'] = []
    items = json.loads(session.get('items', '[]')) 
    items.append(item)
    session['items'] = json.dumps(items)
    return jsonify(session['items'])

@app.route('/remove/<item>')
def remove_item(item):
    if 'items' not in session:
        session['items'] = []
    items = json.loads(session.get('items', '[]')) 
    items.remove(item)
    session['items'] = json.dumps(items)
    return jsonify(session['items'])

@app.route('/getitems')
def get_items():
    items = json.loads(session.get('items', '[]'))
    return jsonify(items)

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
    #skill = flask.request.args.get('skill')
    #max_time = flask.request.args.get('time', type = int)
    ingredient_list = json.loads(ingredient_list) 
    ingredient_list = [ingredient.lower() for ingredient in ingredient_list]
    #if skill or max_time is not None:
        #recipes = db.filter_recipes(skill = skill, max_time = max_time)
    #else:
    recipes = db.return_page_recipes(ingredient_list)
    return render_template('prototype_recommended_recipes.html', recipes=recipes, username=username)

@app.route('/all_recipes', methods=['GET'])
def all_recipes():
    username = auth.authenticate()
    skill = flask.request.args.get('skill', type = str)
    max_time = flask.request.args.get('time', type = int)
    #flask.request.args(ingredient_list)
    if skill or max_time is not None:
        recipes = db.filter_recipes(skill = skill, max_time = max_time)
    else:
        recipes = db.get_all_recipes()
    return render_template('prototype_recommended_recipes.html', recipes=recipes, username=username)

@app.route('/recipe_page', methods=['GET'])
def recipe_page():
    username = auth.authenticate()
    recipe_id = flask.request.args.get("recipe")
    
    recipe = db.return_recipe(recipe_id)
    print("RECIPE", recipe)
    methods = recipe['methods'].replace("\'","\"")
    methods = json.loads(methods)
    #methods = []
    
    return render_template('prototype_recipe_page.html', recipe=recipe, methods=methods, username=username)

@app.route('/add_to_wishlist', methods=['GET', 'POST'])
def add_to_wishlist():
    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']
    if 'wishList' not in session:
        session['wishList'] = db.get_user_wishlist(username)
    wishList = session['wishList']
    recipe_id = flask.request.form.get('recipe_id')

    if recipe_id not in wishList:
        wishList.append(recipe_id)
        db.update_user_wishlist(username, wishList)
        session['wishList'] = wishList
    
    full_wishList = []
    for r_id in wishList:
        recipe = db.return_recipe(r_id)
        if recipe:  
            full_wishList.append(recipe)
    
    return render_template('wishlist.html', wishList=full_wishList, username=username)

@app.route('/profile-page', methods=['GET', 'POST'])
def profile_page():
    username = auth.authenticate()
    user_data = db.get_user(username)
    return render_template('profile_page.html', user_data=user_data)

@app.route('/finished_recipes', methods=['GET'])
def finished_recipes():
    username = auth.authenticate()
    completed_recipes = db.get_completed(username)
    recipes = []
    for recipe_id in completed_recipes:
        recipes.append(db.return_recipe(recipe_id))
    return render_template('prototype_finished_recipes.html', recipes = recipes)

@app.route('/favorite_recipes', methods = ['GET'])
def favorite_recipes():
    username = auth.authenticate
    favRecipes = db.get_favRecipes(username)
    return render_template('prototype_favorite_recipes.html', recipes = favRecipes)

@app.route('/add_to_completed', methods=['GET'])
def add_to_completed():
    recipe_id = flask.request.args.get('completed_recipe')
    username = auth.authenticate()
    user = db.get_user(username)
    completed = user.get('completed', [])
    if recipe_id not in completed:
        completed.append(recipe_id)
        db.update_user_completed(username, completed)

@app.route('/add_to_favorites', methods=['GET'])
def add_to_favorites():
    recipe_id = flask.request.args.get('recipe')
    username = auth.authenticate()
    user = db.get_user(username)
    favorites = user.get('favRecipes', [])
    if recipe_id not in favorites:
        favorites.append(recipe_id)
        db.update_user_favRecipes(username, favorites)

@app.route('/remove_from_favorites', methods=['PATCH'])
def remove_from_favorites():
    recipe_id = flask.request.args.get('recipe')
    username = auth.auntheticate()
    db.remove_favRecipe(username, recipe_id)
    favRecipes = db.get_favRecipes(username)
    return render_template('prototype_favorite_recipes.html', recipes = favRecipes)


    