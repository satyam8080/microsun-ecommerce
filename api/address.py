from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from flask import request
from models.address import Address


@app.route('/address', methods=['POST'])
@jwt_required
def address_store():
    user_id = get_jwt_identity()
    address = request.form.get('address', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    country = request.form.get('country', None)
    pin_code = request.form.get('pin_code', None)

    if not all((address, city, state, country, pin_code)):
        return {"message": "All fields are required"}, 404

    addr = Address(address=address, city=city, state=state, country=country, pin_code=pin_code,
                   user_id=user_id)
    db.session.add(addr)
    db.session.commit()

    res = {"id": addr.id, "address": addr.address, "city": addr.city, "state": addr.state,
           "country": addr.country, "pin_code": addr.pin_code, "user_id": addr.user_id}

    return {"data": res}, 201


@app.route('/address', methods=['GET'])
@jwt_required
def address_get():
    user_id = get_jwt_identity()
    address = Address.query.filter_by(user_id=user_id).all()

    if address:
        res = []
        for addr in address:
            obj = {"id": addr.id, "address": addr.address, "city": addr.city, "state": addr.state,
                   "country": addr.country, "pin_code": addr.pin_code, "user_id": addr.user_id}
            res.append(obj)
        return {"data": res}, 200
    else:
        return {"message": "No address found"}, 404


@app.route('/address/<int:id>', methods=['DELETE'])
@jwt_required
def address_delete(id):
    if Address.query.filter_by(id=id).delete():
        db.session.commit()
        return {"message": "Address deleted successfully"}, 200
    else:
        return {"message": "Address not found to deleted"}, 404
