from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_app.database.db import db
from flask_app import app


db.init_app(app)
app.secret_key = 'your_secret_key'  # For flash messages

enrollments = []  # Stores children data
enrollment_id = 1
roster = []  # Active roster
expired_roster = []  # Expired roster
# Initialize Flask SQLAlchemy


class ExpiredRoster(db.Model):
    __tablename__ = 'roster_exp'
    
        # Define a primary key column
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    date_of_enrollment = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    rate_type = db.Column(db.String(20), nullable=False)