from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(9999), nullable=False)
    description = db.Column(db.String(9999), nullable=False)
    price = db.Column(db.String(9999), nullable=True)
    image = db.Column(db.String(9999), nullable=True)
    expiry = db.Column(db.String(9999), nullable=True)
    category_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
