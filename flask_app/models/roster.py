from flask_app.database.db import db  # Import db from the correct location

class Roster(db.Model):  # This should work now
    __tablename__ = 'roster'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    enrollment_date = db.Column(db.Date, nullable=True)
    expiration_date = db.Column(db.Date, nullable=False)
    rate_type = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Roster {self.first_name} {self.last_name}>'
