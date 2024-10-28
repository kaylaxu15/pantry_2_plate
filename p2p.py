import flask
from flask import Flask, render_template
import DatabaseClient

app = Flask(__name__)
db = DatabaseClient.DatabaseClient()

@app.route('/', methods=['GET'])
@app.route('/?', methods=['GET'])
@app.route('/index', methods=['GET'])
def pantry_page():
    recipes = db.get_all_recipes()
    return render_template('prototype_pantry.html', recipes=recipes)







