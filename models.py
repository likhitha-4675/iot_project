from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    otp = db.Column(db.String(6))
    otp_generated_time = db.Column(db.DateTime, default=datetime.utcnow)
    otp_used_time = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean, default=False)
    data_used = db.Column(db.Float, default=0.0)
    internet_speed = db.Column(db.Float)
