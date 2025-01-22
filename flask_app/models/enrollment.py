from flask import Flask, request, jsonify, send_file
import flask_app
from flask_app.database.db import db
from datetime import datetime, timedelta
import os

# Ensure Enrollment Forms directory exists
ENROLLMENT_FORMS_DIR = os.path.join(os.getcwd(), "documents", "Enrollment Forms")
os.makedirs(ENROLLMENT_FORMS_DIR, exist_ok=True)

class Enrollment(db.Model):
    __tablename__ = 'Enrollment'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    date_of_enrollment = db.Column(db.Date, nullable=True)
    expiration_date = db.Column(db.Date, nullable=False)
    rate_type = db.Column(db.String(20), nullable=True)

