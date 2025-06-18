from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Contact(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    name = db.Column(db.String(100), nullable=False)  # type: ignore
    email = db.Column(db.String(120), nullable=False)  # type: ignore
    subject = db.Column(db.String(200))  # type: ignore
    message = db.Column(db.Text, nullable=False)  # type: ignore
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # type: ignore

    def __repr__(self):
        return f'<Contact {self.name}>'

class Appointment(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    full_name = db.Column(db.String(100), nullable=False)  # type: ignore
    email = db.Column(db.String(120), nullable=False)  # type: ignore
    country = db.Column(db.String(100))  # type: ignore
    marks = db.Column(db.String(50))  # type: ignore
    course = db.Column(db.String(200))  # type: ignore
    intake = db.Column(db.String(100))  # type: ignore
    services = db.Column(db.String(500))  # Store as comma-separated values  # type: ignore
    concerns = db.Column(db.Text)  # type: ignore
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # type: ignore

    def __repr__(self):
        return f'<Appointment {self.full_name}>' 