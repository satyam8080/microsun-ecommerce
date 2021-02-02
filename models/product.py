from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    price = db.Column(db.String(512), nullable=True)
    image = db.Column(db.String(256), nullable=True)
    expiry = db.Column(db.String(32), nullable=True)
    category_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
