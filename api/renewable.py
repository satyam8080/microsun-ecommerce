from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from models.order import Order
from models.product import Product
from datetime import date

from app import app


@app.route('/renewable', methods=['GET'])
@jwt_required
def renewable():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(desc(Order.created_at)).all()
    res = []

    for order in orders:
        product = Product.query.filter_by(id=order.product_id).first()
        string = str(order.created_at)
        chunks = string[0:10]
        string1 = str(product.expiry)

        year, month, day = chunks.split('-')
        y, m = string1.split('-')
        startDate = date(int(year), int(month), int(day))
        endDate = date(startDate.year + int(y), startDate.month + int(m), startDate.day)

        obj = {"product_id": product.id, "purchased_on": order.created_at, "renew_at": endDate,
               "order_id": order.id}
        res.append(obj)

    return {"data": res}, 200
