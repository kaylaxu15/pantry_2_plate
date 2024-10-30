import flask
from flask import Flask, render_template
import DatabaseClient
import pandas as pd

app = Flask(__name__)
db = DatabaseClient.DatabaseClient()

@app.route('/', methods=['GET'])
@app.route('/?', methods=['GET'])
@app.route('/index', methods=['GET'])
def pantry_page():
    ingredient_dicts = pd.read_csv('webscraping/output/processed_recipes_data_2024-10-22.csv')["ingredients_dict"]
    all_keys = set()
    for ingredient_dict in ingredient_dicts:
        all_keys.update(eval(ingredient_dict).keys())
    ingredients = sorted(list(all_keys))

    ingredients = ["Apples", "Eggs", "Milk", "Chicken", "Beef", "Sesame Oil", "Olive Oil", "Butter"]
    return render_template('prototype_pantry.html', ingredients=ingredients)




