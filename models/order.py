from app import db
from datetime import datetime
from enum import Enum


class OrdStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    REFUND = "REFUND"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    COMPLETED = "COMPLETED"
    REJECT = "REJECT"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, default=0, nullable=True)
    transaction_id = db.Column(db.String(512), nullable=True)
    mode = db.Column(db.String(32), nullable=True)
    status = db.Column(db.Enum(OrdStatus), nullable=False)
    order_status = db.Column(db.Enum(OrderStatus), default="PENDING", nullable=False)
    employee_id = db.Column(db.String(32), default=None, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
