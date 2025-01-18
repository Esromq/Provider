from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


