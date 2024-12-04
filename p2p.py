import flask
from flask import Flask, render_template, session, jsonify, request
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
import re

db = DatabaseClient.DatabaseClient()

dotenv.load_dotenv()
app.secret_key = os.environ['APP_SECRET_KEY']

cloudinary.config( 
    cloud_name = os.environ['CLOUDINARY_CLOUD_NAME'], 
    api_key = os.environ['CLOUDINARY_API_KEY'], 
    api_secret = os.environ['CLOUDINARY_API_SECRET'], 
    secure=True
)

@app.route('/', methods=['GET'])
@app.route('/?', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = auth.authenticate()
    db.insert_user(emailId=username, password='')
    return render_template('landing_page.html', username=username)

@app.route('/pantry', methods=['GET'])
def pantry_page():
    username = auth.authenticate()
    ingredients = pd.read_csv('webscraping/output/ingredients_list.csv')
    ingredients = ingredients.values.tolist()
    ingredients = np.squeeze(ingredients)
    pantry_items = db.get_user_inventory(username)
    return render_template('prototype_pantry.html', ingredients=ingredients, pantry_items = pantry_items, username=username)

@app.route('/pantry/save', methods=['POST'])
def save_pantry_items():
    username = auth.authenticate()
    data = request.get_json()
    pantry_items = data.get('pantry_items', [])
    db.update_user_inventory(username, pantry_items)
    return jsonify({'success': True})

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
    return render_template('prototype_recommended_recipes.html', recipes=recipes, username=username, recommended=True)

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
    return render_template('prototype_recommended_recipes.html', recipes=recipes, username=username, recommended=False)

@app.route('/recipe_page', methods=['GET'])
def recipe_page():
    username = auth.authenticate()
    recipe_id = flask.request.args.get("recipe")
    
    recipe = db.return_recipe(recipe_id)

    #methods = recipe['methods'].replace("[,]+ \'", ", \"")
    #methods = recipe['methods'].replace("n\"t", "n\'t")
    #methods = recipe['methods'].replace("\'", "\"")
  
    #methods = json.loads(methods)
    #methods = []
    
    return render_template('prototype_recipe_page.html', recipe=recipe, username=username)

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

@app.route('/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist():
    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']
    
    if 'wishList' not in session:
        session['wishList'] = db.get_user_wishlist(username)
    wishList = session['wishList']
    
    recipe_id = flask.request.form.get('recipe_id')

    if recipe_id in wishList:
        wishList.remove(recipe_id)
        db.update_user_wishlist(username, wishList)
        session['wishList'] = wishList

    full_wishList = []
    for r_id in wishList:
        recipe = db.return_recipe(r_id)
        if recipe:
            full_wishList.append(recipe)

    return render_template('wishlist.html', wishList=full_wishList, username=username)
@app.route('/groceries', methods=['GET'])
def groceries_display():
    username = auth.authenticate()
    groceryList = session['groceryList']
    return render_template('grocery_list.html', groceryList=groceryList, username=username)

@app.route('/add_to_groceries', methods=['POST']) 
def add_to_groceries():
    groceries = flask.request.form['groceries']
    
    #print("GROCERIES", groceries)
    groceries = groceries.replace("\'", "\"")
    ing_list = json.loads(groceries)

    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']
    if 'groceryList' not in session:
        session['groceryList'] = db.get_user_grocerylist(username)
    groceryList = session['groceryList']

    for ingredient in ing_list:
        if ingredient not in groceryList:
            groceryList.append(ingredient)
    db.update_user_grocerylist(username, groceryList)
    session['groceryList'] = groceryList
    
    return render_template('grocery_list.html', groceryList=groceryList, username=username)

# update grocery list in session
@app.route('/remove_from_groceries', methods=['POST'])
def remove_from_groceries():
    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']
    
    item = request.get_json()
    if 'groceryList' not in session:
        session['groceryList'] = db.get_user_grocerylist(username)
    groceryList = session['groceryList']

    if item in groceryList:
        groceryList.remove(item)
    db.update_user_grocerylist(username, groceryList)
    session['groceryList'] = groceryList
    

@app.route('/profile_page', methods=['GET', 'POST'])
def profile_page():
    username = auth.authenticate()
    if request.method == 'POST':
        updated_restrictions = request.form.getlist('restriction')
        db.delete_user_restrictions(username)
        db.update_user_restrictions(username, updated_restrictions)
    user_data = db.get_user(username)
    return render_template('profile_page.html', user_data=user_data)

@app.route('/add_to_completed', methods=['GET', 'POST'])
def add_to_completed():
    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']
    if 'completed' not in session:
        session['completed'] = db.get_user_completed(username)
    completed = session['completed']
    recipe_id = flask.request.form.get('recipe_id')

    if recipe_id not in completed:
        completed.append(recipe_id)
        db.update_user_completed(username, completed)
        session['completed'] = completed
    
    full_completed = []
    for r_id in completed:
        recipe = db.return_recipe(r_id)
        if recipe:
            full_completed.append(recipe)

    return render_template('prototype_finished_recipes.html', completed=full_completed, username=username)


@app.route('/add_to_favorites', methods=['GET', 'POST'])
def add_to_favorites():
    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']
    if 'favRecipes' not in session:
        session['favRecipes'] = db.get_user_favRecipes(username)
    favRecipes = session['favRecipes']
    recipe_id = flask.request.form.get('recipe_id')

    if recipe_id not in favRecipes:
        favRecipes.append(recipe_id)
        db.update_user_favRecipes(username, favRecipes)
        session['favRecipes'] = favRecipes
    
    full_favRecipes = []
    for r_id in favRecipes:
        recipe = db.return_recipe(r_id)
        if recipe:
            full_favRecipes.append(recipe)

    return render_template('prototype_favorite_recipes.html', favRecipes=full_favRecipes, username=username)

@app.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']
    
    if 'favRecipes' not in session:
        session['favRecipes'] = db.get_user_favRecipes(username)
    favRecipes = session['favRecipes']
    
    recipe_id = flask.request.form.get('recipe_id')

    if recipe_id in favRecipes:
        favRecipes.remove(recipe_id)
        db.update_user_favRecipes(username, favRecipes)
        session['favRecipes'] = favRecipes

    full_favRecipes = []
    for r_id in favRecipes:
        recipe = db.return_recipe(r_id)
        if recipe:
            full_favRecipes.append(recipe)

    return render_template('prototype_favorite_recipes.html', favRecipes=full_favRecipes, username=username)

@app.route('/add_review', methods=['POST'])
def add_review():
    if 'username' not in session:
        session['username'] = auth.authenticate()
    username = session['username']

    recipe_id = flask.request.form.get('recipe_id')
    review = flask.request.form.get('review')
    print("REVIEW", review)
    print("RECIPE_ID", recipe_id)

    reviews = db.get_user_reviews(username)
    reviews[recipe_id] = review
    db.update_user_reviews(username, reviews)

    json_doc = json.dumps(review)
    response = flask.make_response(json_doc)
    response.headers['Content-Type'] = 'application/json'

    return response
    



    