from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, app
from flask_app.database.db import db  # Import the db instance
from datetime import datetime
from flask_app.models.claims import claims, MealCount, Receipt

import logging
logging.basicConfig(level=logging.DEBUG)

claims_bp = Blueprint('claims', __name__, url_prefix='/claims')

@claims_bp.route("/claims", methods=["GET"])
def claims_page():
    """Display the claims page or return claims data."""
    try:
        # Check if the request is expecting JSON (e.g., from JavaScript)
        if request.headers.get("Accept") == "application/json":
            claims_data = claims.query.all()  # Fetch data from the database
            claims_list = [
                {
                    "id": claim.id,
                    "purchase_cost": claim.purchase_cost,
                    "purchase_date": claim.purchase_date.strftime("%Y-%m-%d"),
                    "paid_to": claim.paid_to,
                    "purchase_type": claim.purchase_type,
                }
                for claim in claims_data
            ]
            return jsonify({"claims": claims_list})  # Return JSON response

        # Otherwise, render the HTML template for regular browser requests
        return render_template("claims.html")

    except Exception as e:
        return jsonify({"error": "Failed to fetch claims data"}), 500


# PUT: Update a specific claim (Single resource)
@claims_bp.route('/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    claim = claims.query.get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404

    data = request.get_json()
    if 'description' in data:
        claim.description = data['description']
    if 'status' in data:
        claim.status = data['status']

    db.session.commit()
    return jsonify(claim.to_dict()), 200


# DELETE: Delete a specific claim (Single resource)
@claims_bp.route('/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    claim = claims.query.get(claim_id)
    if not claim:
        return jsonify({"error": "Claim not found"}), 404

    db.session.delete(claim)
    db.session.commit()
    return jsonify({"message": "Claim deleted"}), 200


@claims_bp.route('/add-claim', methods=['POST'])
def add_claim():
    # Parse incoming data
    data = request.json
    # Save the data to the database or perform processing
    return jsonify({"message": "Claim added successfully!", "status": "success"})


@claims_bp.route('/submit_claim', methods=['POST'])
def submit_claim():
    try:
        print(request.headers)
        
        # Parse the incoming JSON data
        data = request.get_json()
        print("Received data:", data)

        # Extract values from the JSON data
        meal_count = data.get('meal_count')  # Example: "9"
        purchase_type = data.get('purchase_type')  # Example: "Food"
        purchase_date = data.get('purchase_date')  # Example: "2025-01-01"
        paid_to = data.get('paid_to')  # Example: "walmart"
        receipt_amount = data.get('receipt_amount')  # Example: ["10"]
        receipt_date = data.get('receipt_date')  # Example: ["2025-01-01"]
        operating_cost = float(data.get('operating_cost', 0))

        logger = logging.getLogger(__name__)  # Correct logging
        logger.debug(f"Sending data: {data}")

        # Check if content type is application/json
        if request.content_type != 'application/json':
            return jsonify({"error": "415 Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not 'application/json'."}), 415

        # Check if the 'receipts' key exists in the incoming data
        if 'receipts' not in data:
            return jsonify({'error': 'Receipts data is missing from the request'}), 400

        # Extract the receipts data
        receipt_data = data['receipts']

        # Ensure receipt_data is a list
        if not isinstance(receipt_data, list):
            return jsonify({'error': 'Receipts data should be a list'}), 400

        # Create a list of Receipt objects and ensure claim_id is set
        receipts = []
        for receipt in receipt_data:
            purchase_date = datetime.strptime(receipt['purchase_date'], "%Y-%m-%d").date()

            # Ensure the necessary fields are present in each receipt
            if all(key in receipt for key in ['date', 'paid_to', 'purchase_type', 'purchase_date', 'purchase_cost']):
                # Create the receipt with the claim_id associated
                receipts.append(Receipt(
                    date=receipt['date'],
                    paid_to=receipt['paid_to'],
                    purchase_type=receipt['purchase_type'],
                    purchase_date=purchase_date,
                    purchase_cost=receipt['purchase_cost'],
                    claim_id=None  # Placeholder for claim ID; will set later
                ))
            else:
                return jsonify({'error': 'Missing fields in receipt data'}), 400

        # Create the claim object
        new_claim = claims(
            operating_cost=operating_cost,
            meal_count=meal_count,
            receipts=receipts
        )

        # Add the new claim to the session and commit
        db.session.add(new_claim)
        db.session.commit()

        # Now that the claim is committed, update the claim_id in receipts
        for receipt in receipts:
            receipt.claim_id = new_claim.id  # Set claim_id for each receipt

        # Commit the changes for the receipts
        db.session.commit()

        return jsonify({'message': 'Claim submitted successfully!'}), 201

    except Exception as e:
        # Handle any exceptions
        return jsonify({'error': str(e)}), 400
