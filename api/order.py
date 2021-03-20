import os
import platform
import subprocess

import pdfkit
from flask import request, render_template, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from gunicorn.config import User
from sqlalchemy import desc

from app import app, db
from models.address import Address
from models.cart import Cart
from models.order import Order
from models.product import Product
from models.user import User

mail = Mail(app)


def _get_pdfkit_config():
    if platform.system() == 'Windows':
        return pdfkit.configuration(
            wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
    else:
        WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')],
                                           stdout=subprocess.PIPE).communicate()[0].strip()
        return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)


def send_bill(id, transaction_id):
    user = User.query.filter_by(id=id).first()
    to = user.email
    subject = "Order Confirmed"
    template = "new_user"
    link = "https://microsun-ecommerce-backend.herokuapp.com/" + "pdf/get/" + transaction_id
    msg = Message(subject, recipients=[to], sender=app.config['FLASKY_MAIL_SENDER'])
    msg.html = render_template(template + '.html', user=user, link=link)
    mail.send(msg)

    return None


def details(transaction_id):
    orders = Order.query.filter_by(transaction_id=transaction_id).all()
    price = 0
    res = []
    for order in orders:
        user = User.query.filter_by(id=order.user_id).first()
        address = Address.query.filter_by(user_id=order.user_id).first()

        obj = {"order_id": order.id, "order_on": order.created_at, "user_name": user.name, "email": user.email,
               "billing_address": address.address, "state": address.state, "country": address.country,
               "pin_code": address.pin_code, "payment_mode": order.mode, "status": order.status,
               "transaction_id": transaction_id}
        res.append(obj)
        price += int(order.price)

    temp = {"total_price": price}
    res.append(temp)
    return res


def product_detail(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        obj = {"product_name": product.name}
        return obj


def shipping_address():
    user_id = get_jwt_identity()
    address = Address.query.filter_by(user_id=user_id).order_by(desc(Address.created_at)).first()
    if address:
        return address.address


def serialization(order):
    res = {"id": order.id, "user_id": order.user_id, "product_id": order.product_id, "price": order.price,
           "transaction_id": order.transaction_id, "mode": order.mode, "status": order.status,
           "added_on": order.created_at, "product_name": product_detail(order.product_id)['product_name'],
           "shipping_address": shipping_address(), "username": username(order.user_id)}
    return res


def username(id):
    user = User.query.filter_by(id=id).first()
    return user.name


@app.route('/orders', methods=['POST'])
@jwt_required
def order_store():
    user_id = get_jwt_identity()
    transaction_id = request.form.get('transaction_id', None)
    mode = request.form.get('mode', None)
    status = request.form.get('status', None)

    address = request.form.get('address', None)
    city = request.form.get('city', None)
    state = request.form.get('state', None)
    country = request.form.get('country', None)
    pin_code = request.form.get('pin_code', None)

    if not all((user_id, status, mode, transaction_id, address, city, state, country, pin_code)):
        return {"message": "All fields are required"}, 404

    addr = Address(address=address, city=city, state=state, country=country, pin_code=pin_code,
                   user_id=user_id)
    db.session.add(addr)
    db.session.commit()

    carts = Cart.query.filter_by(user_id=user_id).all()
    for cart in carts:
        orde = Order(user_id=user_id, product_id=cart.product_id, transaction_id=transaction_id, mode=mode,
                     status=status, price=cart.price)
        db.session.add(orde)
        db.session.commit()
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    orders = Order.query.filter_by(transaction_id=transaction_id).all()
    res = []
    if orders:
        for order in orders:
            res.append(serialization(order))

    send_bill(user_id, transaction_id)
    return {"data": res}, 201


@app.route('/orders', methods=['GET'])
@jwt_required
def history():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(desc(Order.created_at)).all()

    if orders:
        res = []
        for order in orders:
            res.append(serialization(order))
        return {"data": res}, 200
    else:
        return {"message": "No order history found"}, 404


@app.route('/pdf/get/<string:transaction_id>', methods=['GET', 'POST'])
def get_pdf(transaction_id):
    detail = details(transaction_id)

    orders = Order.query.filter_by(transaction_id=transaction_id).all()
    products = []
    for order in orders:
        product = Product.query.filter_by(id=order.product_id).first()
        obj = {"product_name": product.name, "price": order.price}
        products.append(obj)

    filename = "OrderDetail.pdf"
    rendered = render_template('invoice.html', detail=detail, products=products)
    pdf = pdfkit.from_string(rendered, False, configuration=_get_pdfkit_config(), options=None)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = "attachment;filename=\"" + filename + "\""

    return response
