from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from flask import request
from models.cards import Card


def serialization(card):
    res = {"id": card.id, "user_id": card.user_id, "card_type": card.type, "card_number": card.card_number,
           "first_name": card.first_name, "last_name": card.last_name, "expiry_date": card.expiry_date,
           "cvv": card.cvv, "bank": card.bank, "postal_code": card.postal_code, "state": card.state}
    return res


@app.route('/cards', methods=['POST'])
@jwt_required
def store():
    user_id = get_jwt_identity()
    card_type = request.form.get('type', None)
    card_number = request.form.get('card_number', None)
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    cvv = request.form.get('cvv', None)
    bank = request.form.get('bank', None)
    postal_code = request.form.get('postal_code', None)
    state = request.form.get('state', None)
    expiry_date = request.form.get('expiry_date', None)

    if expiry_date:
        year, month, day = expiry_date.split('-')
        expiry_date = date(int(year), int(month), int(day))

    card = Card(user_id=user_id, type=card_type, card_number=card_number, first_name=first_name, last_name=last_name,
                expiry_date=expiry_date, cvv=cvv, bank=bank, postal_code=postal_code, state=state)
    db.session.add(card)
    db.session.commit()

    return {"data": serialization(card)}, 200


@app.route('/cards', methods=['GET'])
@jwt_required
def get():
    user_id = get_jwt_identity()
    card = Card.query.filter_by(user_id=user_id).first()
    if card:
        return {"data": serialization(card)}, 200
    else:
        return {"message": "No card found"}, 404


@app.route('/cards', methods=['DELETE'])
@jwt_required
def delete():
    user_id = get_jwt_identity()
    if Card.query.filter_by(user_id=user_id).delete():
        return {"message": "Card deleted successfully"}, 200
    else:
        return {"message": "Card not found for deletion"}, 404
