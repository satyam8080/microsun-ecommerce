from datetime import date

from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app, db
from flask import request
from models.cart import Cart
from models.product import Product


def product_detail(id):
    product = Product.query.filter_by(id=id).first()

    if product:
        obj = {"product_name": product.name, "product_description": product.description}
        return obj
    else:
        return None


def expiry(product_id, created_at):
    product = Product.query.filter_by(id=product_id).first()

    string = str(created_at)
    chunks = string[0:10]
    string1 = str(product.expiry)

    year, month, day = chunks.split('-')
    y, m = string1.split('-')
    startDate = date(int(year), int(month), int(day))
    endDate = date(startDate.year + int(y), startDate.month + int(m), startDate.day)
    return endDate


def serialization(cart):
    res = {"id": cart.id, "user_id": cart.user_id, "product_id": cart.product_id,
           "product_name": product_detail(cart.product_id)['product_name'],
           "product_description": product_detail(cart.product_id)['product_description'],
           "expiry": None, "price": cart.price, "added_on": cart.created_at}
    return res


@app.route('/cart', methods=['POST'])
@jwt_required
def cart_store():
    user_id = get_jwt_identity()
    product_id = request.form.get('product_id', None)
    p = Product.query.filter_by(id=product_id).first()
    price = p.price

    if not all((user_id, product_id, price)):
        return {"message": "All fields are required"}, 404

    crt = Cart(user_id=user_id, product_id=product_id, price=price)
    db.session.add(crt)
    db.session.commit()

    return {"data": serialization(crt)}, 201


@app.route('/cart', methods=['GET'])
@jwt_required
def cart_get():
    user_id = get_jwt_identity()
    carts = Cart.query.filter_by(user_id=user_id).all()

    if carts:
        res = []
        for cart in carts:
            res.append(serialization(cart))
        return {"data": res}, 200
    else:
        return {"message": "No item in cart"}, 404


@app.route('/cart/<int:id>', methods=['DELETE'])
@jwt_required
def cart_delete(id):
    if Cart.query.filter_by(id=id).delete():
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200
    else:
        return {"message": "No product found for delete"}, 404
