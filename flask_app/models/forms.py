from flask import Blueprint, request, jsonify, Flask
from app.static import EnrollmentForm, Claim
from app.services.validation import validate_form
from app.services.claim_calculator import calculate_reimbursement
from flask_app.database.db import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')
