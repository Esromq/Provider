from flask import Blueprint, request, jsonify

forms_bp = Blueprint('forms', __name__)

@forms_bp.route('/submit-enrollment', methods=['POST'])
def submit_enrollment():
    data = request.json
    validation = validate_form(data)
    if not validation['valid']:
        return jsonify({'error': validation['message']}), 400

    form = EnrollmentForm(**data)
    form.save()
    return jsonify({'message': 'Enrollment form submitted successfully!'})

@forms_bp.route('/calculate-claims', methods=['POST'])
def calculate_claims():
    data = request.json
    result = calculate_reimbursement(data)
    return jsonify(result)
