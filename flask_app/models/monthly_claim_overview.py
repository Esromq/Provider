from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_app.database.db import db 



class Daycare(db.Model):
    __tablename__ = 'daycare'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(200), nullable=False)
    
    # Back reference for MonthlyClaimOverview
    monthly_claims = db.relationship('MonthlyClaimOverview', back_populates='daycare')

class MonthlyClaimOverview(db.Model):
    __tablename__ = 'monthly_claim_overview'

    id = db.Column(db.Integer, primary_key=True)
    daycare_id = db.Column(db.Integer, db.ForeignKey('daycare.id'), nullable=False)  # FK to Daycare table

    # Correct relationship with back_populates
    daycare = db.relationship('Daycare', back_populates='monthly_claims')

    month = db.Column(db.String(20), nullable=False)  # e.g., "January 2025"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Overview fields
    working_days = db.Column(db.Integer, nullable=False, default=0)
    total_meals_served = db.Column(db.JSON, nullable=False, default={})  # e.g., {'breakfast': 120, 'lunch': 200, ...}
    income_status_percentages = db.Column(db.JSON, nullable=False, default={})  # e.g., {'free': 50, 'reduced': 30, 'paid': 20}

    # Calendar breakdown fields
    daily_totals = db.Column(db.JSON, nullable=False, default={})  # e.g., {'2025-01-01': {...}, ...}

    # Status fields
    status = db.Column(db.String(50), nullable=False, default='New')  # 'New', 'In Review', etc.
    admin_message = db.Column(db.String(255), nullable=True)

    # Header info
    daycare_name = db.Column(db.String(100), nullable=False)
    daycare_address = db.Column(db.String(255), nullable=False)
    daycare_contact = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<MonthlyClaim {self.daycare_name} - {self.month}>'

    # Example method to calculate meal percentages (if needed)
    def calculate_meal_percentages(self):
        total = sum(self.total_meals_served.values())
        if total == 0:
            return {}
        return {meal: (count / total) * 100 for meal, count in self.total_meals_served.items()}
