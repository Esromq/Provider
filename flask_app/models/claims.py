from flask import Flask, jsonify
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.database.db import db  # Import the db instance from db.py


class claims(db.Model):
    __tablename__ = 'claims'
    id = db.Column(db.Integer, primary_key=True)
    operating_cost = db.Column(db.Float, nullable=True)
    meal_count = db.Column(db.Integer)
    total_meals_served = db.Column(db.Float, nullable=True)

    
    def __init__(self, operating_cost=None, receipts=None, meal_count=None):
        self.operating_cost = operating_cost
        self.receipts = receipts or []
        self.meal_count = meal_count

        
    receipts = db.relationship('Receipt', backref='claim', lazy=True)
class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(120))
    paid_to = db.Column(db.String(120))
    purchase_cost = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    paid_to = db.Column(db.String(255), nullable=False)
    purchase_type = db.Column(db.String(255), nullable=False)
    claim_id = db.Column(db.Integer, db.ForeignKey('claims.id'), nullable=False)



class MealCount(db.Model):
    __tablename__ = 'meal_counts'
    id = db.Column(db.Integer, primary_key=True)
    child_breakfast_1yrs = db.Column(db.Integer, default=0)
    child_breakfast_2yrs = db.Column(db.Integer, default=0)
    child_breakfast_3_5yrs = db.Column(db.Integer, default=0)
    child_breakfast_6_12yrs = db.Column(db.Integer, default=0)

    child_AMSnack_1yrs = db.Column(db.Integer, default=0)
    child_AMSnack_2yrs = db.Column(db.Integer, default=0)
    child_AMSnack_3_5yrs = db.Column(db.Integer, default=0)
    child_AMSnack_6_12yrs = db.Column(db.Integer, default=0)

    child_Lunch_1yrs = db.Column(db.Integer, default=0)
    child_Lunch_2yrs = db.Column(db.Integer, default=0)
    child_Lunch_3_5yrs = db.Column(db.Integer, default=0)
    child_Lunch_6_12yrs = db.Column(db.Integer, default=0)

    child_PMSnack_1yrs = db.Column(db.Integer, default=0)
    child_PMSnack_2yrs = db.Column(db.Integer, default=0)
    child_PMSnack_3_5yrs = db.Column(db.Integer, default=0)
    child_PMSnack_6_12yrs = db.Column(db.Integer, default=0)

    child_Supper_1yrs = db.Column(db.Integer, default=0)
    child_Supper_2yrs = db.Column(db.Integer, default=0)
    child_Supper_3_5yrs = db.Column(db.Integer, default=0)
    child_Supper_6_12yrs = db.Column(db.Integer, default=0)

    infant_breakfast_birth_3mos = db.Column(db.Integer, default=0)
    infant_breakfast_4_7mos = db.Column(db.Integer, default=0)
    infant_breakfast_8_12mos = db.Column(db.Integer, default=0)

    infant_AMSnack_birth_3mos = db.Column(db.Integer, default=0)
    infant_AMSnack_4_7mos = db.Column(db.Integer, default=0)
    infant_AMSnack_8_12mos = db.Column(db.Integer, default=0)

    infant_Lunch_birth_3mos = db.Column(db.Integer, default=0)
    infant_Lunch_4_7mos = db.Column(db.Integer, default=0)
    infant_Lunch_8_12mos = db.Column(db.Integer, default=0)

    infant_PMSnack_birth_3mos = db.Column(db.Integer, default=0)
    infant_PMSnack_4_7mos = db.Column(db.Integer, default=0)
    infant_PMSnack_8_12mos = db.Column(db.Integer, default=0)

    infant_Supper_birth_3mos = db.Column(db.Integer, default=0)
    infant_Supper_4_7mos = db.Column(db.Integer, default=0)
    infant_Supper_8_12mos = db.Column(db.Integer, default=0)

    @property
    def totals(self):
        return {
            "child_breakfast_total": sum([
                self.child_breakfast_1yrs,
                self.child_breakfast_2yrs,
                self.child_breakfast_3_5yrs,
                self.child_breakfast_6_12yrs,
            ]),
            "child_AMSnack_total": sum([
                self.child_AMSnack_1yrs,
                self.child_AMSnack_2yrs,
                self.child_AMSnack_3_5yrs,
                self.child_AMSnack_6_12yrs,
            ]),
            "child_Lunch_total": sum([
                self.child_Lunch_1yrs,
                self.child_Lunch_2yrs,
                self.child_Lunch_3_5yrs,
                self.child_Lunch_6_12yrs,
            ]),
            "child_PMSnack_total": sum([
                self.child_PMSnack_1yrs,
                self.child_PMSnack_2yrs,
                self.child_PMSnack_3_5yrs,
                self.child_PMSnack_6_12yrs,
            ]),
            "child_Supper_total": sum([
                self.child_Supper_1yrs,
                self.child_Supper_2yrs,
                self.child_Supper_3_5yrs,
                self.child_Supper_6_12yrs,
            ]),
            "infant_breakfast_total": sum([
                self.infant_breakfast_birth_3mos,
                self.infant_breakfast_4_7mos,
                self.infant_breakfast_8_12mos,
            ]),
            "infant_AMSnack_total": sum([
                self.infant_AMSnack_birth_3mos,
                self.infant_AMSnack_4_7mos,
                self.infant_AMSnack_8_12mos,
            ]),
            "infant_Lunch_total": sum([
                self.infant_Lunch_birth_3mos,
                self.infant_Lunch_4_7mos,
                self.infant_Lunch_8_12mos,
            ]),
            "infant_PMSnack_total": sum([
                self.infant_PMSnack_birth_3mos,
                self.infant_PMSnack_4_7mos,
                self.infant_PMSnack_8_12mos,
            ]),
            "infant_Supper_total": sum([
                self.infant_Supper_birth_3mos,
                self.infant_Supper_4_7mos,
                self.infant_Supper_8_12mos,
            ]),
        }




