from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from flask_app.database.db import db  # Import the db instance from db.py

# Initialize Flask SQLAlchemy

class daycare(db.Model):
    __tablename__ = 'daycare' 

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(200), nullable=False)

    # Back reference for the relationship
monthly_claims = db.relationship('MonthlyClaimOverview', back_populates='daycare')

    