from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import or_
import os
import re
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import pandas as pd
import csv
import pandas as pd


load_dotenv()
app = Flask(__name__, template_folder='templates',static_folder='static')

# Get the current directory
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

bcrypt = Bcrypt(app)
# server_session=Session(app)
db = SQLAlchemy(app)

class Recipes(db.Model):
    __tablename__ = 'Recipes'
    # RecipeMeta
    Metano = db.Column(db.Integer)
    Srno = db.Column(db.Integer, primary_key=True)
    RecipeName = db.Column(db.String)
    TranslatedRecipeName = db.Column(db.String)
    Ingredients = db.Column(db.String)
    TranslatedIngredients = db.Column(db.String)
    PrepTimeInMins = db.Column(db.Integer)
    CookTimeInMins = db.Column(db.Integer)
    TotalTimeInMins = db.Column(db.Integer)
    Servings = db.Column(db.Integer)
    Cuisine = db.Column(db.String)
    Course = db.Column(db.String)
    Diet = db.Column(db.String)
    Instructions = db.Column(db.String)
    TranslatedInstructions = db.Column(db.String)
    URL = db.Column(db.String)
    # RecipeOverview
    uri = db.Column(db.String)
    yield_ = db.Column(db.Float)  # 'yield' is a reserved keyword in Python
    calories = db.Column(db.Float)
    totalCO2Emissions = db.Column(db.Float)
    co2EmissionsClass = db.Column(db.String)
    totalWeight = db.Column(db.Float)
    dietLabels = db.Column(db.String)
    healthLabels = db.Column(db.String)
    cautions = db.Column(db.String)
    cuisineType = db.Column(db.String)
    mealType = db.Column(db.String)
    dishType = db.Column(db.String)
    # RecipeDetailed
    ENERC_KCAL = db.Column(db.Float)
    ENERC_KCAL_perc = db.Column(db.Float)
    FAT = db.Column(db.Float)
    FAT_perc = db.Column(db.Float)
    FASAT = db.Column(db.Float)
    FASAT_perc = db.Column(db.Float)
    PROCNT = db.Column(db.Float)
    PROCNT_perc = db.Column(db.Float)
    CHOLE = db.Column(db.Float)
    CHOLE_perc = db.Column(db.Float)
    CHOCDF = db.Column(db.Float)
    CHOCDF_perc = db.Column(db.Float)
    FIBTG = db.Column(db.Float)
    FIBTG_perc = db.Column(db.Float)
    FATRN = db.Column(db.Float)
    FAMS = db.Column(db.Float)
    FAPU = db.Column(db.Float)
    SUGAR = db.Column(db.Float)
    CHOCDF_net = db.Column(db.Float)
    NA = db.Column(db.Float)
    NA_perc = db.Column(db.Float)
    CA = db.Column(db.Float)
    CA_perc = db.Column(db.Float)
    FE = db.Column(db.Float)
    FE_perc = db.Column(db.Float)
    ZN = db.Column(db.Float)
    ZN_perc = db.Column(db.Float)
    VITC = db.Column(db.Float)
    VITC_perc = db.Column(db.Float)
    THIA = db.Column(db.Float)
    THIA_perc = db.Column(db.Float)
    NIA = db.Column(db.Float)
    NIA_perc = db.Column(db.Float)
    VITB6A = db.Column(db.Float)
    VITB6A_perc = db.Column(db.Float)
    MG = db.Column(db.Float)
    MG_perc = db.Column(db.Float)
    K = db.Column(db.Float)
    K_perc = db.Column(db.Float)
    P = db.Column(db.Float)
    P_perc = db.Column(db.Float)
    VITA_RAE = db.Column(db.Float)
    VITA_RAE_perc = db.Column(db.Float)
    RIBF = db.Column(db.Float)
    RIBF_perc = db.Column(db.Float)
    FOLDFE = db.Column(db.Float)
    FOLDFE_perc = db.Column(db.Float)
    VITB12 = db.Column(db.Float)
    VITB12_perc = db.Column(db.Float)
    VITD = db.Column(db.Float)
    VITD_perc = db.Column(db.Float)
    TOCPHA = db.Column(db.Float)
    TOCPHA_perc = db.Column(db.Float)
    VITK1 = db.Column(db.Float)
    VITK1_perc = db.Column(db.Float)
    WATER = db.Column(db.Float)
    FOLFD = db.Column(db.Float)
    FOLAC = db.Column(db.Float)


# Flask Bcrypt
bcrypt = Bcrypt()

def validate_password(password):
    '''Password Validator:
    Conditions for password validation:
    Minimum 8 characters.
    The alphabet must be between [a-z]
    At least one alphabet should be of Upper Case [A-Z]
    At least 1 number or digit between [0-9].
    At least 1 character from [ _ or @ or $ ]. '''

    if len(password) < 8 or re.search("\s" , password):  
        return False  
    if not (re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) ):
        return False  
    return True  

def split_list(input_list, n):
    length = len(input_list)
    return [input_list[i*length // n: (i+1)*length // n] for i in range(n)]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/browse')
def browse():
    recipes = Recipes.query.with_entities(Recipes.Srno, Recipes.RecipeName).all()
    return render_template('browse.html', recipes=recipes)

@app.route('/recipe-details/<int:id>')
def recipe_details(id):
    recipe = Recipes.query.filter_by(Srno=id).all()
    if recipe:
        return render_template('recipe.html', recipe=recipe[0].__dict__)
    return render_template('recipe.html', recipe="null")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        recipes = Recipes.query.filter(or_(Recipes.RecipeName.like(f'%{search}%'),
                                            Recipes.TranslatedRecipeName.like(f'%{search}%'),
                                            Recipes.Ingredients.like(f'%{search}%'),
                                            Recipes.Cuisine.like(f'%{search}%'),
                                            Recipes.cuisineType.like(f'%{search}%')
                                            )).with_entities(Recipes.Srno, Recipes.RecipeName).all()
        return render_template('search.html', recipes=recipes)
    return render_template('search.html',recipes=None)

@app.route('/meal_planner', methods=['GET', 'POST'])
def meal_planner():
    if request.method == 'POST':
        duration = int(request.form['duration'])
        kcal_goal = float(request.form['kcal_goal'])
        meals_per_day = int(request.form['meals_per_day'])
        recipes = Recipes.query.filter(Recipes.ENERC_KCAL <= kcal_goal/meals_per_day).with_entities(Recipes.Srno, Recipes.RecipeName, Recipes.ENERC_KCAL).order_by(Recipes.ENERC_KCAL.desc()).limit(meals_per_day*duration).all()
        recipe_list = split_list(recipes, duration)
        return render_template('meal_planner.html', recipe_list=recipe_list,meals_per_day=meals_per_day)
    return render_template('meal_planner.html',recipe_list=None)

if __name__=='__main__':
    app.run(port=5005)