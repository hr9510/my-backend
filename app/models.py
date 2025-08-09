from app import db
from sqlalchemy.inspection import inspect
from sqlalchemy import  Column, Integer, String

class Menu(db.Model):
    __tablename__ = "restauntMenu"
    id = db.Column(db.Integer, primary_key=True)
    dish_price = Column(db.Integer)

    def to_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
    
class PreparedDish(db.Model):
    __tablename__ = "prepared_dish"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
    
class OrderedDish(db.Model):
    __tablename__ = "orderedDish"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
    
class Setdishes(db.Model):
    __tablename__ = "Setdishes"
    id = db.Column(db.Integer, primary_key=True)
    setCooked = db.Column(db.String, nullable=False)
    setOrdered = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}