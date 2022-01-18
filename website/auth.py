from flask import Blueprint,render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("logIn.html")

@auth.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@auth.route('/expiry')
def expiry():
    return render_template("expiry.html")

@auth.route('/signUp')
def signUp():
    return render_template("signUp.html")