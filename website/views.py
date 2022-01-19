from cgitb import html
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/recipe')
def recipe():
    return render_template("recipe.html")





