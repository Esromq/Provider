from mimetypes import init
from time import strptime
from flask import Flask, Blueprint, request, jsonify, send_file, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_app.database.db import db
from flask_app.models.claims import Claims, Receipt, MealCount
import os
from datetime import datetime

claims_bp = Blueprint("claims", __name__)

CLAIMS_DIR = os.path.join(os.getcwd(), "viewClaims", "Claims")
os.makedirs(CLAIMS_DIR, exist_ok=True)

@claims_bp.route('/claims/test', methods=['GET'])
def test():
    return "Route works!"

@claims_bp.route("/claims", methods=["GET"])
def claim_view():
    """Render the claim page."""
    return render_template("claims.html")

@claims_bp.route("/get-claims", methods=["GET"])
def get_claims():
    """Fetch and return the current claim."""
    try:
        # Parse incoming data
        data = request.get_json()
        print("Received data:", data)  # Debugging

        # Query all claims
        claims_data = Claims.query.all()

        # Format data for the frontend
        claims = [
            {
                "id": claim.id,
                "paid_to": claim.paid_to,
                "purchase_type": claim.purchase_type,
                "purchase_cost": claim.purchase_cost,
                "purchase_date": claim.purchase_date.strftime("%Y-%m-%d"),
                "operating_cost": claim.operating_cost,
                "infant_AMSnack_birth_3mos": claim.infant_AMSnack_birth_3mos,
                "infant_AMSnack_4_7mos": claim.infant_AMSnack_4_7mos,
                "infant_AMSnack_8_12mos": claim.infant_AMSnack_8_12mos,
                "child_breakfast_1yrs": claim.child_breakfast_1yrs,
                "child_breakfast_2yrs": claim.child_breakfast_2yrs,
                "child_breakfast_3_5yrs": claim.child_breakfast_3_5yrs,
                "child_breakfast_6_12yrs": claim.child_breakfast_6_12yrs,
                "child_AMSnack_1yrs": claim.child_AMSnack_1yrs,
                "child_AMSnack_2yrs": claim.child_AMSnack_2yrs,
                "child_AMSnack_3_5yrs": claim.child_AMSnack_3_5yrs,
                "child_AMSnack_6_12yrs": claim.child_AMSnack_6_12yrs,
                "infant_Lunch_birth_3mos": claim.infant_Lunch_birth_3mos,
                "infant_Lunch_4_7mos": claim.infant_Lunch_4_7mos,
                "infant_Lunch_8_12mos": claim.infant_Lunch_8_12mos,
                "child_Lunch_1yrs": claim.child_Lunch_1yrs,
                "child_Lunch_2yrs": claim.child_Lunch_2yrs,
                "child_Lunch_3_5yrs": claim.child_Lunch_3_5yrs,
                "child_Lunch_6_12yrs": claim.child_Lunch_6_12yrs,
                "infant_PMSnack_birth_3mos": claim.infant_PMSnack_birth_3mos,
                "infant_PMSnack_4_7mos": claim.infant_PMSnack_4_7mos,
                "infant_PMSnack_8_12mos": claim.infant_PMSnack_8_12mos,
                "child_PMSnack_1yrs": claim.child_PMSnack_1yrs,
                "child_PMSnack_2yrs": claim.child_PMSnack_2yrs,
                "child_PMSnack_3_5yrs": claim.child_PMSnack_3_5yrs,
                "child_PMSnack_6_12yrs": claim.child_PMSnack_6_12yrs,
                "infant_Supper_birth_3mos": claim.infant_Supper_birth_3mos,
                "infant_Supper_4_7mos": claim.infant_Supper_4_7mos,
                "infant_Supper_8_12mos": claim.infant_Supper_8_12mos,
                "child_Supper_1yrs": claim.child_Supper_1yrs,
                "child_Supper_2yrs": claim.child_Supper_2yrs,
                "child_Supper_3_5yrs": claim.child_Supper_3_5yrs,
                "child_Supper_6_12yrs": claim.child_Supper_6_12yrs,
                "infant_breakfast_birth_3mos": claim.infant_breakfast_birth_3mos,
                "infant_breakfast_4_7mos": claim.infant_breakfast_4_7mos,
                "infant_breakfast_8_12mos": claim.infant_breakfast_8_12mos,
            }
            for claim in claims_data
        ]

        # Debug log to verify fetched data
        print(f"Fetched Claim Data: {claims}")

        # Return the formatted data as JSON
        return jsonify(claims), 200
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching claims data: {e}")
        return jsonify({"error": "Failed to fetch claims data"}), 500


@claims_bp.route('/claims/submit-claims', methods=['POST'])
def submit_claims():
    try:
        data = request.get_json()  # Parse incoming JSON
        print("Received data:", data)  # Log received data

        if not data:
            return jsonify({"error": "No data provided"}), 400

        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format, expected a list."}), 400

        # Iterate over each claim and validate/process
        for claim in data:
            # Validate required fields
            required_fields = [
                'id',
                'paid_to',
                'purchase_type',
                'purchase_cost',
                'purchase_date',
                'operating_cost',
                'infant_AMSnack_birth_3mos',
                'infant_AMSnack_4_7mos',
                'infant_AMSnack_8_12mos',
                'child_breakfast_1yrs',
                'child_breakfast_2yrs',
                'child_breakfast_3_5yrs',
                'child_breakfast_6_12yrs',
                'child_AMSnack_1yrs',
                'child_AMSnack_2yrs',
                'child_AMSnack_3_5yrs',
                'child_AMSnack_6_12yrs',
                'infant_Lunch_birth_3mos',
                'infant_Lunch_4_7mos',
                'infant_Lunch_8_12mos',
                'child_Lunch_1yrs',
                'child_Lunch_2yrs',
                'child_Lunch_3_5yrs',
                'child_Lunch_6_12yrs',
                'infant_PMSnack_birth_3mos',
                'infant_PMSnack_4_7mos',
                'infant_PMSnack_8_12mos',
                'child_PMSnack_1yrs',
                'child_PMSnack_2yrs',
                'child_PMSnack_3_5yrs',
                'child_PMSnack_6_12yrs',
                'infant_Supper_birth_3mos',
                'infant_Supper_4_7mos',
                'infant_Supper_8_12mos',
                'child_Supper_1yrs',
                'child_Supper_2yrs',
                'child_Supper_3_5yrs',
                'child_Supper_6_12yrs',
                'infant_breakfast_birth_3mos',
                'infant_breakfast_4_7mos',
                'infant_breakfast_8_12mos',
            ]
            if not all(field in claim for field in required_fields):
                return jsonify({"error": f"Missing required fields in claim: {claim}"}), 400

            # Process and save the claim
            new_claim = Claims(
                id=claim['id'],
                paid_to=claim['paid_to'],
                purchase_type=claim['purchase_type'],
                purchase_cost=claim['purchase_cost'],
                purchase_date=claim['purchase_date'],
                operating_cost=claim['operating_cost'],
                infant_AMSnack_birth_3mos=claim['infant_AMSnack'].get('birth_3mos', 0),
                infant_AMSnack_4_7mos=claim['infant_AMSnack'].get('four_7mos', 0),
                infant_AMSnack_8_12mos=claim['infant_AMSnack'].get('eight_12mos', 0),
                child_breakfast_1yrs=claim['child_breakfast'].get('one_year', 0),
                child_breakfast_2yrs=claim['child_breakfast'].get('two_years', 0),
                child_breakfast_3_5yrs=claim['child_breakfast'].get('three_five_years', 0),
                child_breakfast_6_12yrs=claim['child_breakfast'].get('six_twelve_years', 0),
                child_AMSnack_1yrs=claim['child_AMSnack'].get('one_year', 0),
                child_AMSnack_2yrs=claim['child_AMSnack'].get('two_years', 0),
                child_AMSnack_3_5yrs=claim['child_AMSnack'].get('three_five_years', 0),
                child_AMSnack_6_12yrs=claim['child_AMSnack'].get('six_twelve_years', 0),
                infant_Lunch_birth_3mos=claim['infant_Lunch'].get('birth_3mos', 0),
                infant_Lunch_4_7mos=claim['infant_Lunch'].get('four_7mos', 0),
                infant_Lunch_8_12mos=claim['infant_Lunch'].get('eight_12mos', 0),
                child_Lunch_1yrs=claim['child_Lunch'].get('one_year', 0),
                child_Lunch_2yrs=claim['child_Lunch'].get('two_years', 0),
                child_Lunch_3_5yrs=claim['child_Lunch'].get('three_five_years', 0),
                child_Lunch_6_12yrs=claim['child_Lunch'].get('six_twelve_years', 0),
                infant_PMSnack_birth_3mos=claim['infant_PMSnack'].get('birth_3mos', 0),
                infant_PMSnack_4_7mos=claim['infant_PMSnack'].get('four_7mos', 0),
                infant_PMSnack_8_12mos=claim['infant_PMSnack'].get('eight_12mos', 0),
                child_PMSnack_1yrs=claim['child_PMSnack'].get('one_year', 0),
                child_PMSnack_2yrs=claim['child_PMSnack'].get('two_years', 0),
                child_PMSnack_3_5yrs=claim['child_PMSnack'].get('three_five_years', 0),
                child_PMSnack_6_12yrs=claim['child_PMSnack'].get('six_twelve_years', 0),
                infant_Supper_birth_3mos=claim['infant_Supper'].get('birth_3mos', 0),
                infant_Supper_4_7mos=claim['infant_Supper'].get('four_7mos', 0),
                infant_Supper_8_12mos=claim['infant_Supper'].get('eight_12mos', 0),
                child_Supper_1yrs=claim['child_Supper'].get('one_year', 0),
                child_Supper_2yrs=claim['child_Supper'].get('two_years', 0),
                child_Supper_3_5yrs=claim['child_Supper'].get('three_five_years', 0),
                child_Supper_6_12yrs=claim['child_Supper'].get('six_twelve_years', 0),
                infant_breakfast_birth_3mos=claim['infant_breakfast'].get('birth_3mos', 0),
                infant_breakfast_4_7mos=claim['infant_breakfast'].get('four_7mos', 0),
                infant_breakfast_8_12mos=claim['infant_breakfast'].get('eight_12mos', 0),
                meal_count=claim.get('meal_count', 0),  # Assuming meal_count is an integer or similar
            )

            # Add the new claim to the session
            db.session.add(new_claim)

        # Commit all changes at once
        db.session.commit()
        return jsonify({"message": "Claims submitted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@claims_bp.route('/claims/show-claim', methods=['GET'])
def show_claims():
    try:
        claims = Claims.query.all()
        result = [
            {
                "id": r.id,
                "paid_to": r.paid_to,
                "purchase_type": r.purchase_type,
                "purchase_cost": r.purchase_cost,
                "purchase_date": r.purchase_date.strftime("%Y-%m-%d"),
                "operating_cost": r.operating_cost,
                "infant_AMSnack_birth_3mos": r.infant_AMSnack_birth_3mos,
                "infant_AMSnack_4_7mos": r.infant_AMSnack_4_7mos,
                "infant_AMSnack_8_12mos": r.infant_AMSnack_8_12mos,
                "child_breakfast_1yrs": r.child_breakfast_1yrs,
                "child_breakfast_2yrs": r.child_breakfast_2yrs,
                "child_breakfast_3_5yrs": r.child_breakfast_3_5yrs,
                "child_breakfast_6_12yrs": r.child_breakfast_6_12yrs,
                "child_AMSnack_1yrs": r.child_AMSnack_1yrs,
                "child_AMSnack_2yrs": r.child_AMSnack_2yrs,
                "child_AMSnack_3_5yrs": r.child_AMSnack_3_5yrs,
                "child_AMSnack_6_12yrs": r.child_AMSnack_6_12yrs,
                "infant_Lunch_birth_3mos": r.infant_Lunch_birth_3mos,
                "infant_Lunch_4_7mos": r.infant_Lunch_4_7mos,
                "infant_Lunch_8_12mos": r.infant_Lunch_8_12mos,
                "child_Lunch_1yrs": r.child_Lunch_1yrs,
                "child_Lunch_2yrs": r.child_Lunch_2yrs,
                "child_Lunch_3_5yrs": r.child_Lunch_3_5yrs,
                "child_Lunch_6_12yrs": r.child_Lunch_6_12yrs,
                "infant_PMSnack_birth_3mos": r.infant_PMSnack_birth_3mos,
                "infant_PMSnack_4_7mos": r.infant_PMSnack_4_7mos,
                "infant_PMSnack_8_12mos": r.infant_PMSnack_8_12mos,
                "child_PMSnack_1yrs": r.child_PMSnack_1yrs,
                "child_PMSnack_2yrs": r.child_PMSnack_2yrs,
                "child_PMSnack_3_5yrs": r.child_PMSnack_3_5yrs,
                "child_PMSnack_6_12yrs": r.child_PMSnack_6_12yrs,
                "infant_Supper_birth_3mos": r.infant_Supper_birth_3mos,
                "infant_Supper_4_7mos": r.infant_Supper_4_7mos,
                "infant_Supper_8_12mos": r.infant_Supper_8_12mos,
                "child_Supper_1yrs": r.child_Supper_1yrs,
                "child_Supper_2yrs": r.child_Supper_2yrs,
                "child_Supper_3_5yrs": r.child_Supper_3_5yrs,
                "child_Supper_6_12yrs": r.child_Supper_6_12yrs,
                "infant_breakfast_birth_3mos": r.infant_breakfast_birth_3mos,
                "infant_breakfast_4_7mos": r.infant_breakfast_4_7mos,
                "infant_breakfast_8_12mos": r.infant_breakfast_8_12mos,
            }
            for r in claims
        ]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@claims_bp.route("/claims/remove-claims/<int:claims_id>", methods=["DELETE"], endpoint="remove_claim_from_claims")
def remove_claims(claims_id):
    """Remove a claim from the claims by its ID."""
    try:
        # Find the claim in the database
        claim = Claims.query.get(claims_id)
        if not claim:
            return jsonify({"success": False, "message": "Claim not found"}), 404
        # Remove the claim
        db.session.delete(claim)
        db.session.commit()
        return jsonify({"success": True, "message": "Claim removed successfully"}), 200
    except Exception as e:
        print(f"Error removing claim: {e}")
        return jsonify({"success": False, "message": "An error occurred while removing the claim"}), 500