from app import db
from datetime import datetime


class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, default=None, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    state = db.Column(db.String(32), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    pin_code = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
