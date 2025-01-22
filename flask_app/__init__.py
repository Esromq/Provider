from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import logging
logging.basicConfig(level=logging.DEBUG)

from flask_app.database.db import db
from flask_app.models.roster import Roster
from flask_app.routes.enrollment_routes import enrollment_bp
from flask_app.routes.roster_routes import roster_bp
from flask_app.routes.monthly_claim_routes import monthly_claim_bp
from flask_app.routes.daycare_routes import daycare_bp
from flask_app.routes.claims_routes import claims_bp
from flask_app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Configure the app
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'database.db')}"    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key'
    db.init_app(app)
    with app.app_context():
        db.create_all()  # This will create all tables defined in your models

    # Initialize extensions
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(enrollment_bp, url_prefix='/enrollment')
    app.register_blueprint(roster_bp, url_prefix='/roster')
    app.register_blueprint(claims_bp, url_prefix='/claims')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(daycare_bp, url_prefix='/daycare')
    app.register_blueprint(monthly_claim_bp, url_prefix='/monthly-claim')

    print(app.url_map)
    
    return app