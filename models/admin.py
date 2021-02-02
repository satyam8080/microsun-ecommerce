from app import db
from datetime import datetime


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    password = db.Column(db.Binary(128), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    mobile = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
