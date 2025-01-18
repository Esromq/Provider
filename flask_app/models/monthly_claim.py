from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_app.database.db import db
from flask_app.routes.monthly_claim_routes import monthly_claim_bp


class MonthlyClaim(db.Model):
    __tablename__ = 'monthly_claims'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)  # e.g., "January 2025"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Meal data and other information
    total_meals_served = db.Column(db.JSON, nullable=True, default=dict)
    income_status_percentages = db.Column(db.JSON, nullable=True, default=dict)
    daycare_name = db.Column(db.String(100), nullable=False)
    daycare_address = db.Column(db.String(200), nullable=False)
    daycare_contact = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<MonthlyClaim {self.daycare_name} - {self.month}>"

    @classmethod
    def create_claim(cls, month, total_meals_served, income_status_percentages, daycare_name, daycare_address, daycare_contact):
        """Helper method to create a new claim."""
        new_claim = cls(
            month=month,
            total_meals_served=total_meals_served,
            income_status_percentages=income_status_percentages,
            daycare_name=daycare_name,
            daycare_address=daycare_address,
            daycare_contact=daycare_contact
        )
        db.session.add(new_claim)
        db.session.commit()
        return new_claim
