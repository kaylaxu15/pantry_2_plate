from flask import Flask, render_template
import DatabaseClient
import pandas as pd
import numpy as np

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
    # blah
    ingredients = ['150g salted butter, plus 2 tbsp ', 'marmalade ', 
                   'black tea bags ', '3 eggs', '150g golden caster sugar', 
                   '1 tbsp honey ', '160g self-raising flour ', 'madeleine tins']
    
    return render_template('prototype_recipes.html')


# @app.route('/all_recipes', methods=['GET'])
# def results_page():
#     # blah
#     return render_template('prototype_all_recipes.html')






