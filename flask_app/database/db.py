from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from . import db  # Import the db instance from your app

# Initialize SQLAlchemy
db = SQLAlchemy()


# You can later initialize it in the application context with init_app()

# Initialize Flask SQLAlchemy

def init_db(app):
    """
    Initialize the database with the given Flask app.

    - Bind the app to SQLAlchemy.
    - Create all tables in the database if they do not exist.
    """
    db.init_app(app)  # Bind the app to SQLAlchemy
    with app.app_context():
        db.create_all()  # Create tables
        
        # Create engine and session for direct SQLAlchemy usage
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
session = Session()