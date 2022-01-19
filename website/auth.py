from flask import Blueprint,render_template, request, flash
import mysql.connector

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data=request.form
    print(data)
    return render_template("logIn.html")

@auth.route('/dashboard', )
def dashboard():
    return render_template("dashboard.html")

@auth.route('/expiry')
def expiry():
    return render_template("expiry.html")

@auth.route('/signUp',methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        
        if len(email) < 4:
            flash('Enter a valid email!', category = 'error')
        elif len(firstName) < 3:
            flash('First name must be greater than 2 characters',category='error')
        elif password != password1:
            flash('Passwords don\'t match',category='error')
        elif len(password) < 8:
            flash('Password must be atleast 8 characters',category='error')
        else:
            mydb = mysql.connector.connect(host="localhost", user="root",passwd="cybereagle0602",database="hax")
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

