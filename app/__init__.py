from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#set up for file uploading
app.config['UPLOAD_FOLDER'] = "app/static/models/"

#now import the routes, models etc
from app import routes, models

