from flask import Blueprint, render_template
from flask_app.models.roster_exp import ExpiredRoster

roster_exp_bp = Blueprint('roster_exp_routes', __name__)

@roster_exp_bp.route('/roster-exp', methods=['GET'])
def roster_exp():
    expired_sentries = ExpiredRoster.query.all()
    return render_template('roster_exp.html', expired_roster=expired_entries)

