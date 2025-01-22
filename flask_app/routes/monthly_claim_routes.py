from flask import Blueprint, jsonify
from flask_app.models.claims import Claims

monthly_claim_bp = Blueprint('monthly_claim', __name__)

@monthly_claim_bp.route('/monthly-claim/<id>', methods=['GET'])
def get_monthly_claim(id):
    try:
        claim = Claims.query.filter_by(id=id).first()
        if claim:
            result = {
                "month 1": claim.January,
                "month 2": claim.February,
                "month 3": claim.March,
            }
            return jsonify(result), 200
        else:
            return jsonify({"error": "Claim not found"}), 404
    except Exception as e:
        # Log the exception
        print("Error:", str(e))
        return jsonify({"error": "An error occurred"}), 500