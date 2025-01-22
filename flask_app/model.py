from flask import Flask, jsonify
from flask_app.database.db import db
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry
from flask_login import UserMixin
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship




from datetime import datetime
app = Flask(__name__, static_url_path='/static')

bcrypt = Bcrypt(app)

# Optional: Use registry for advanced mappings if needed
mapper_registry = registry()
Base = mapper_registry.generate_base()

# Define models
# class MyModel(Base):
 #   __tablename__ = 'my_model'
  #  id = Column(Integer, primary_key=True)
   # name = Column(String(100), nullable=False)
    
   
class Claims(db.Model):
    __tablename__ = 'claims'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'))
    meal_counts_id = Column(Integer, ForeignKey('meal_counts.id'), nullable=False)
    
    # Specify the foreign_keys argument to clarify which foreign key to use
    meal_counts = relationship("MealCount", back_populates="claims", foreign_keys=[meal_counts_id], remote_side=[meal_counts_id])
    receipt = relationship("Receipt", back_populates="claims", foreign_keys=[receipt_id])  # Specify foreign_keys here

    def __repr__(self):
        return f'<Claims {self.id} {self.meal_counts} {self.receipt}>'

class MealCount(db.Model):
    __tablename__ = 'meal_counts'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    claims_id = Column(Integer, ForeignKey('claims.id'))  # ForeignKey reference to Claims
    claims = relationship("Claims", back_populates="meal_counts", foreign_keys=[claims_id], remote_side=[claims_id])
    
    # Meal count fields
    infant_breakfast_birth_3mos = Column(Integer, default=0)
    infant_breakfast_4_7mos = Column(Integer, default=0)
    infant_breakfast_8_12mos = Column(Integer, default=0)    
    child_breakfast_1yrs = Column(Integer, default=0)
    child_breakfast_2yrs = Column(Integer, default=0)
    child_breakfast_3_5yrs = Column(Integer, default=0)
    child_breakfast_6_12yrs = Column(Integer, default=0)
    infant_AMSnack_birth_3mos = Column(Integer, default=0)
    infant_AMSnack_4_7mos = Column(Integer, default=0)
    infant_AMSnack_8_12mos = Column(Integer, default=0)
    child_AMSnack_1yrs = Column(Integer, default=0)
    child_AMSnack_2yrs = Column(Integer, default=0)
    child_AMSnack_3_5yrs = Column(Integer, default=0)
    child_AMSnack_6_12yrs = Column(Integer, default=0)
    infant_Lunch_birth_3mos = Column(Integer, default=0)
    infant_Lunch_4_7mos = Column(Integer, default=0)
    infant_Lunch_8_12mos = Column(Integer, default=0)
    child_Lunch_1yrs = Column(Integer, default=0)
    child_Lunch_2yrs = Column(Integer, default=0)
    child_Lunch_3_5yrs = Column(Integer, default=0)
    child_Lunch_6_12yrs = Column(Integer, default=0)
    infant_PMSnack_birth_3mos = Column(Integer, default=0)
    infant_PMSnack_4_7mos = Column(Integer, default=0)
    infant_PMSnack_8_12mos = Column(Integer, default=0)
    child_PMSnack_1yrs = Column(Integer, default=0)
    child_PMSnack_2yrs = Column(Integer, default=0)
    child_PMSnack_3_5yrs = Column(Integer, default=0)
    child_PMSnack_6_12yrs = Column(Integer, default=0)
    infant_Supper_birth_3mos = Column(Integer, default=0)
    infant_Supper_4_7mos = Column(Integer, default=0)
    infant_Supper_8_12mos = Column(Integer, default=0)
    child_Supper_1yrs = Column(Integer, default=0)
    child_Supper_2yrs = Column(Integer, default=0)
    child_Supper_3_5yrs = Column(Integer, default=0)
    child_Supper_6_12yrs = Column(Integer, default=0)
    meal_count = Column(Integer, default=0)
    def __repr__(self):
        return f'<MealCount {self.id} {self.meal_count}>'
def __repr__(self):
        return f'<MealCount {self.id} {self.meal_count}>'

class Receipt(db.Model):
    __tablename__ = 'receipt'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    claims_id = Column(Integer, ForeignKey('claims.id'))  # ForeignKey reference to Claims
    paid_to = Column(String(120))
    purchase_type = Column(String(255), nullable=False)
    purchase_cost = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    operating_cost = Column(Float, nullable=True)

    # Specify the foreign_keys argument to clarify which foreign key to use
    claims = relationship('Claims', back_populates='receipt', foreign_keys=[claims_id])

    def __init__(self, operating_cost=None, receipt=None, meal_counts=None):
        self.operating_cost = operating_cost
        self.receipt = receipt or []
        self.meal_counts = meal_counts

    def __repr__(self):
        return f'<Receipt {self.id} {self.purchase_type}>'
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

class daycare(db.Model):
    __tablename__ = 'daycare' 
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(200), nullable=False)

class Enrollment(db.Model):
    __tablename__ = 'Enrollment'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    date_of_enrollment = db.Column(db.Date, nullable=True)
    expiration_date = db.Column(db.Date, nullable=False)
    rate_type = db.Column(db.String(20), nullable=True)

class MonthlyClaimOverview(db.Model):
    __tablename__ = 'monthly_claim_overview'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    daycare_id = db.Column(db.Integer, db.ForeignKey('daycare.id'), nullable=False)  # FK to Daycare table
    daycare = db.relationship('Daycare', back_populates='monthly_claims')  # Relationship with Daycare

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

class MonthlyClaim(db.Model):
    __tablename__ = 'monthly_claims'
    __table_args__ = {'extend_existing': True}

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

class Roster(db.Model):
    __tablename__ = 'roster'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    date_of_enrollment = db.Column(db.Date, nullable=True)
    expiration_date = db.Column(db.Date, nullable=False)
    rate_type = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Roster {self.first_name} {self.last_name}>'


class ExpiredRoster(db.Model):
    __tablename__ = 'roster_exp'
    __table_args__ = {'extend_existing': True}


        # Define a primary key column
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    date_of_enrollment = db.Column(db.Date, nullable=True)
    expiration_date = db.Column(db.Date, nullable=False)
    rate_type = db.Column(db.String(20), nullable=True)
    
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    daycare_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


