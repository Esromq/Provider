from flask import Flask, Blueprint, jsonify, request
from flask_app.database.db import db  # Import the db instance from db.py
from flask_app.models.enrollment import Enrollment
from flask_app.models.roster import Roster
from datetime import datetime, timedelta
import os
from pydf import generate_pdf

enrollment_bp = Blueprint('enrollment', __name__)


ENROLLMENT_FORMS_DIR = os.path.join(os.getcwd(), "documents", "Enrollment Forms")
os.makedirs(ENROLLMENT_FORMS_DIR, exist_ok=True)

@enrollment_bp.route('/enrollment/submit-enroll', methods=['POST'])
def submit_enroll():
    try:
        data = request.get_json()  # Parse incoming JSON
        print("Received data:", data)  # Log received data

        if not data:
            return jsonify({"error": "No data provided"}), 400

        if isinstance(data, list):  # Expected data as a list
            for child in data:
                # Validate that each required field exists and is a string
                if not all(isinstance(child.get(key), str) for key in ['first_name', 'last_name', 'dob', 'enrollment_date']):
                    return jsonify({"error": "Invalid or missing fields in data. Ensure all fields are strings."}), 400
                
                # Parse dates, ensuring the arguments are strings
                dob = datetime.strptime(child['dob'], '%Y-%m-%d')
                enrollment_date = datetime.strptime(child['enrollment_date'], '%Y-%m-%d')
                expiration_date = enrollment_date + timedelta(days=364)

                # Create a new Roster entry
                new_child = Roster(
                    first_name=child['first_name'],
                    last_name=child['last_name'],
                    dob=dob,
                    enrollment_date=enrollment_date,
                    expiration_date=expiration_date,
                    rate_type=None
                )

                db.session.add(new_child)
            
            # Commit all changes at once
            db.session.commit()
            return jsonify({"message": "Enrollment submitted successfully"}), 200

        else:
            return jsonify({"error": "Invalid data format, expected list."}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@enrollment_bp.route('/enrollment/get-enrollments', methods=['GET'])
def get_enrollments():
    # Example GET endpoint to retrieve current enrollments
    enrollments = Roster.query.all()
    enrollment_data = [
        {
            "first_name": enrollment.first_name,
            "last_name": enrollment.last_name,
            "dob": enrollment.dob.strftime('%Y-%m-%d'),
            "enrollment_date": enrollment.date_of_enrollment.strftime('%Y-%m-%d'),
            "expiration_date": enrollment.expiration_date.strftime('%Y-%m-%d'),
            "rate_type": enrollment.rate_type
        } for enrollment in enrollments
    ]
    return jsonify({"enrollments": enrollment_data}), 200

@enrollment_bp.route('enrollment/get-roster', methods=['GET'])
def get_roster():
    roster = Roster.query.all()  # Query all entries in the roster table
    return jsonify([{
            "first_name": r.first_name,
            "last_name": r.last_name,
            "dob": r.dob,
            "enrollment_date": r.enrollment_date,
            "expiration_date": r.expiration_date
        } for r in roster]), 200
    # Example response
        # Fetch the roster data from the database or other sources
    roster_data = {"children": [{"first_name": "Esrom", "last_name": "Quarterman", "dob": "2025-01-01", "enrollment_date": "2025-01-10"}]}
    return jsonify({"month": "January", "children": []})


@enrollment_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404
