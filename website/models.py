from email.policy import default
from enum import unique
from time import timezone
from sqlalchemy import PrimaryKeyConstraint
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Table(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(69))
    quantity = db.Column(db.String(69))
    currentDate = db.Column(db.DateTime(timezone=True),default=func.now)
    expiryDate = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin) :
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(69),unique=True)
    password = db.Column(db.String(150))
    table = db.relationship('Table')