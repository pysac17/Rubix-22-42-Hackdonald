from flask import Blueprint,render_template, request, flash
import mysql.connector
import re
from sqlalchemy import true   

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

def check(email):   
    if(re.search(regex,email)):   
        return True  
    else:   
        return False 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        mydb = mysql.connector.connect(host="localhost", user="root",passwd="1234",database="hax")
        mycursor=mydb.cursor()
        mycursor.execute("SELECT * FROM temp_users WHERE EMAIL = %s AND PASSWORD = %s",(email,password))
        for i in mycursor:
            if i == False:
                return 
            else:
                return render_template("dashboard.html")
        
        flash('Invalid credentials', category='error')
    return render_template("logIn.html")

@auth.route('/dashboard', )
def dashboard():
    return render_template("dashboard.html")

@auth.route('/expiry')
def expiry():
    if request.method == 'POST':
        Product = request.form.get('Name')
        Quantity = request.form.get('Quantity')
        expiryDate = request.form.get('expiryDate')
        uploadFile = request.form.get('uploadFile')
        
        mydb = mysql.connector.connect(host="localhost", user="root",passwd="1234",database="hax")
        mycursor=mydb.cursor()
        mycursor.execute("INSERT INTO food_db (Name, quanFridge, currExpiry) VALUES (%s,%s,%s)",(Product, Quantity, expiryDate))
        mydb.commit()
        mycursor.execute("SELECT * FROM food_db")
        for i in mycursor:
            print(i)

    return render_template("expiry.html")

@auth.route('/signUp',methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        
        if not check(email):
            flash('Enter a valid email!', category = 'error')
        elif len(firstName) < 3:
            flash('First name must be greater than 2 characters',category='error')
        elif password != password1:
            flash('Passwords don\'t match',category='error')
        elif len(password) < 8:
            flash('Password must be atleast 8 characters',category='error')
        else:
            mydb = mysql.connector.connect(host="localhost", user="root",passwd="1234",database="hax")
            mycursor=mydb.cursor()
            mycursor.execute("INSERT INTO temp_users (FIRSTNAME,LASTNAME,EMAIL,PASSWORD) VALUES (%s,%s,%s,%s)",(firstName,lastName,email,password))
            mydb.commit()
            
            mycursor.execute("SELECT * FROM temp_users")
            for i in mycursor:
                print(i)

            flash('Account created!',category='success')

    return render_template("signUp.html")

@auth.route('/')
def logout():
    return render_template("home.html")

