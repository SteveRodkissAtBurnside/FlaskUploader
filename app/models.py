from flask.json import jsonify
from app import db
from dataclasses import dataclass

@dataclass
class ModelFile(db.Model):
    id:int
    filename:str
    #now the columns
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80))


