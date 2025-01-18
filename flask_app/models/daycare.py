from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from flask_app.database.db import db  # Import the db instance from db.py

# Initialize Flask SQLAlchemy


    # Back reference for the relationship
monthly_claims = db.relationship('MonthlyClaimOverview', back_populates='daycare')

    