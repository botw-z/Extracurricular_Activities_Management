from config import db
from datetime import datetime
from sqlalchemy import Numeric, Enum

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(Enum('admin', 'user', name='user_roles'), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceHours(db.Model):
    __tablename__ = 'service_hours'
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    service_date = db.Column(db.Date, nullable=False)
    hours_served = db.Column(Numeric(5,2), nullable=False)
    activity_description = db.Column(db.Text)
    status = db.Column(Enum('pending', 'approved', 'rejected', name='status_types'), default='pending')
    verified_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 