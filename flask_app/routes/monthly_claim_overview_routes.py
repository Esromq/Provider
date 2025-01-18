from flask import Blueprint, request, render_template, jsonify, Flask
from flask_app.models.monthly_claim_overview import db, MonthlyClaimOverview
from datetime import datetime

monthly_claim_overview_bp = Blueprint('monthly_claim_overview', __name__)


@monthly_claim_overview_bp.route('/monthly_claim_overview')
def oveview():
    # Check if a claim already exists for the current month
    data = request.json
    existing_claim = MonthlyClaimOverview.query.filter_by(daycare_id=data['daycare_id'], month=data['month']).first()

    if existing_claim:
        return jsonify({'error': 'A claim for this month already exists.'}), 400

    # Create a new MonthlyClaim
    new_claim = MonthlyClaimOverview(
        daycare_id=data['daycare_id'],
        month=data['month'],
        daycare_name=data['daycare_name'],
        daycare_address=data['daycare_address'],
        daycare_contact=data['daycare_contact'],
        working_days=data['working_days'],
        total_meals_served=data['total_meals_served'],
        income_status_percentages=data['income_status_percentages'],
        daily_totals=data['daily_totals']
    )
    db.session.add(new_claim)
    db.session.commit()

    return jsonify({'message': 'Monthly claim created successfully.', 'claim_id': new_claim.id}), 201


@monthly_claim_overview_bp.route('/monthly-claims/<int:claim_id>/edit', methods=['POST'])
def edit_claim(claim_id):
    claim = MonthlyClaimOverview.query.get_or_404(claim_id)
    data = request.json

    # Update claim fields within admin ranges
    claim.working_days = data.get('working_days', claim.working_days)
    claim.total_meals_served = data.get('total_meals_served', claim.total_meals_served)
    claim.income_status_percentages = data.get('income_status_percentages', claim.income_status_percentages)
    claim.daily_totals = data.get('daily_totals', claim.daily_totals)
    claim.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Claim updated successfully.'}), 200


@monthly_claim_overview_bp.route('/monthly-claims/<int:claim_id>/request-review', methods=['POST'])
def request_review(claim_id):
    claim = MonthlyClaimOverview.query.get_or_404(claim_id)
    claim.status = 'In Review'
    db.session.commit()

    # Notify admin (dummy implementation here)
    admin_message = f"{claim.daycare_name} has requested a review of their pre-claim for {claim.month}."
    return jsonify({'message': 'Review requested.', 'admin_message': admin_message}), 200


@monthly_claim_overview_bp.route('/monthly-claims/<int:claim_id>/submit', methods=['POST'])
def submit_final_claim(claim_id):
    claim = MonthlyClaimOverview.query.get_or_404(claim_id)
    if claim.status != 'Passed Review':
        return jsonify({'error': 'Cannot submit final claim. Claim must pass review first.'}), 400

    claim.status = f'Submitted ({claim.month})'
    db.session.commit()
    return jsonify({'message': 'Final claim submitted successfully.'}), 200


@monthly_claim_overview_bp.route('/monthly-claims/<int:claim_id>', methods=['GET'])
def view_claim(claim_id):
    claim = MonthlyClaimOverview.query.get_or_404(claim_id)
    return render_template('view_claim.html', claim=claim)
