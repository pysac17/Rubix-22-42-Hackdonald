from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Table
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, login_manager, logout_user
import mysql.connector
import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

def check(email):   
    if(re.search(regex,email)):   
        return True  
    else:   
        return False 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("logIn.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/dashboard', methods=['GET', 'POST'] )
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@auth.route('/expiry', methods=['GET', 'POST'])
@login_required
def expiry():
    if request.method == ['POST']:
        product = request.form.get('product')
        quantity = request.form.get('quantity')
        currentDate = '20/1/2022'
        expiryDate = request.form.get('expiryDate')
        new_food=Table(product=product,quantity=quantity,currentDate=currentDate, expiryDate= expiryDate)
        db.session.add(new_food)
        db.session.commit()
        flash('Food Added!!', category='success')
    return render_template("expiry.html", user=current_user)

@auth.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password')
        password2 = request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif check(email) != True:
            flash('Invalid email!', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signUp.html", user=current_user)
