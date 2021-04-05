from app import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(9999), nullable=False)
    description = db.Column(db.String(9999), nullable=True)
    photo = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
