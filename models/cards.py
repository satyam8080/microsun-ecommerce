from enum import Enum
from app import db
from datetime import datetime


class Types(str, Enum):
    CREDITCARD = "CREDITCARD"
    DEBITCARD = "DEBITCARD"
    NETBANKING = "NETBANKING"


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, default=0, nullable=True)
    type = db.Column(db.Enum(Types), nullable=True)
    card_number = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    expiry_date = db.Column(db.String(16), nullable=True)
    cvv = db.Column(db.String(8), nullable=True)
    bank = db.Column(db.String(256), nullable=True)
    postal_code = db.Column(db.String(16), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
