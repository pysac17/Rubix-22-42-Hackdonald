from flask import Blueprint,render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("logIn.html")

@auth.route('/dashboard', )
def dashboard():
    return render_template("dashboard.html")

@auth.route('/expiry')
def expiry():
    return render_template("expiry.html")

@auth.route('/signUp',methods=['GET', 'POST'])
def signUp():
    return render_template("signUp.html")

@auth.route('/')
def logout():
    return render_template("home.html")

