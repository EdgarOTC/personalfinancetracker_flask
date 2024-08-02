from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app and to instantiate the flask function as app 
app = Flask(__name__)

# # in-memory database for simplicty 
# posts = [{"title": "Post 1", "content": "This is the content of post 1"}, {"title": "Post 2", "content": "This is the content of post 2"}]

# to replace my in-memory database with a real database
# flask sql alchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FinanceTracker.db'
db = SQLAlchemy(app)

@app.template_filter("get_item")
def get_item(values: dict, id: int):
    res = list(filter(lambda x: x.id == id, values))[0]
    return f"{res.id}-{res.name}"

@app.template_filter("date_format")
def date_format(value, format="%Y-%m-%d"):
    return value.strftime(format)

class Persons(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)    

# class Groups(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)

class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(1), nullable=False)

# class Group_Persons_Category(db.Model):    
#     group = db.ForeignKey(Groups.id)
#     person = db.ForeignKey(Persons.id)
#     category = db.ForeignKey(Categories.id)
#     percentage = db.Column(db.Integer, nullable=False)    

class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    person = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)

    # category = db.Column(db.Integer, nullable=False)
    # person = db.Column(db.Integer, nullable=False)
    # category = db.ForeignKey(Categories.id)
    # person = db.ForeignKey(Persons.id)
   