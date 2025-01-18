from flask import Blueprint, request, render_template, jsonify, Flask
from datetime import datetime
from flask_app.database.db import db
from flask_app.models.claims import claims
import logging
logging.basicConfig(level=logging.DEBUG)


monthly_claim_bp = Blueprint('monthly_claim', __name__)




@monthly_claim_bp.route('/monthly-claim/<id>', methods=['GET'])
def monthly_claim():
    try:
        monthly_claim = Claims.query.all()
        result = [
            {
                "month 1": r.January,  #make link-able to the saved monthly claims resectively
                "month 2": r.February,
                "month 3": r.March,
            }
            for r in Claims
        ]
                
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500