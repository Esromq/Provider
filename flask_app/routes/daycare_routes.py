from flask import Blueprint, request, jsonify, Flask
from flask_app.database.db import db  # Import the db instance from db.py

daycare_bp = Blueprint('daycare', __name__)

app = Flask(__name__, static_url_path='/static')
