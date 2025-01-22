from mimetypes import init
from flask import Flask, Blueprint, request, jsonify, send_file, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_app.database.db import db
from flask_app.models.roster import Roster
from datetime import datetime, timedelta
import os

roster_bp = Blueprint("roster", __name__)

ENROLLMENT_FORMS_DIR = os.path.join(os.getcwd(), "documents", "Enrollment Forms")
os.makedirs(ENROLLMENT_FORMS_DIR, exist_ok=True)

@roster_bp.route("/roster", methods=["GET"])
def roster_view():
    """Render the roster page."""
    return render_template("roster.html")

@roster_bp.route("/get-roster", methods=["GET"])
def get_roster():
    """Fetch and return the current roster."""
    try:
        # Query all children with expiration dates in the future or today
        roster_data = Roster.query.filter(
            Roster.expiration_date >= datetime.utcnow()
        ).all()

        # Format data for the frontend
        roster = [
            {
                "id": child.id,
                "first_name": child.first_name,
                "last_name": child.last_name,
                "dob": child.dob.strftime("%Y-%m-%d"),
                "enrollment_date": child.enrollment_date.strftime("%Y-%m-%d"),
                "expiration_date": child.expiration_date.strftime("%Y-%m-%d"),
            }
            for child in roster_data
        ]

        # Debug log to verify fetched data
        print(f"Fetched Roster Data: {roster}")

        # Return the formatted data as JSON
        return jsonify(roster), 200
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching roster data: {e}")
        return jsonify({"error": "Failed to fetch roster data"}), 500



# Route to display the roster
@roster_bp.route('roster/show-roster', methods=['GET'])
def show_roster():
    try:
        date_of_enrollment = 'enrollment_date'
        roster = Roster.query.all()
        result = [
            {
                "first_name": r.first_name,
                "last_name": r.last_name,
                "dob": r.dob.strftime('%Y-%m-%d'),
                "enrollment_date": r.date_of_enrollment.strftime('%Y-%m-%d'),
                "expiration_date": r.expiration_date,
                "rate_type": r.rate_type,
            }
            for r in roster
        ]
        

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@roster_bp.route("roster/remove-child/<int:child_id>", methods=["DELETE"], endpoint="remove_child_from_roster")
def remove_child(child_id):
    """Remove a child from the roster by their ID."""
    try:
        # Find the child in the database
        child = Roster.query.get(child_id)
        if not child:
            return jsonify({"success": False, "message": "Child not found"}), 404

        # Remove the child
        db.session.delete(child)
        db.session.commit()
        return jsonify({"success": True, "message": "Child removed successfully"}), 200
    except Exception as e:
        print(f"Error removing child: {e}")
        return jsonify({"success": False, "message": "An error occurred while removing the child"}), 500
    

