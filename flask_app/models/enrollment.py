from flask import Flask, request, jsonify, send_file
import flask_app
from flask_app.database.db import db
from fpdf import FPDF
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
    date_of_enrollment = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    rate_type = db.Column(db.String(20), nullable=False)

def generate_pdf(data):
    """Generate a PDF for enrollment information."""
    pdf_file_path = os.path.join(
        ENROLLMENT_FORMS_DIR,
        f"{data['last_name']}_{data['first_name']}_EnrollmentForm.pdf"
    )
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Enrollment Form", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Enrollment Date: {data['enrollment_date']}", ln=True)
    pdf.cell(200, 10, txt=f"Name: {data['first_name']} {data['last_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Date of Birth: {data['dob']}", ln=True)
    pdf.cell(200, 10, txt=f"SSN (Last 4): {data['ssn']}", ln=True)
    pdf.cell(200, 10, txt=f"Occupation: {data['occupation']}", ln=True)
    pdf.cell(200, 10, txt=f"Income: {data['total_income']} ({data['income_method']})", ln=True)
    pdf.cell(200, 10, txt=f"Household Members: {data['household_members']}", ln=True)
    pdf.output(pdf_file_path)
    return pdf_file_path

