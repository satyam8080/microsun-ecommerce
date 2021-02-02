from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy import desc

from app import app, db
from models.address import Address
from models.employee import Employee
from models.order import Order
from models.product import Product


def shipping_address(user_id):
    address = Address.query.filter_by(user_id=user_id).order_by(desc(Address.created_at)).first()
    if address:
        return address.address


def product_detail(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        obj = {"product_name": product.name}
        return obj


def serialization(orders):
    if orders:
        res = []
        temp = []
        for order in orders:
            obj = {"id": order.id, "user_id": order.user_id, "product_id": order.product_id, "price": order.price,
                   "transaction_id": order.transaction_id, "mode": order.mode, "status": order.status,
                   "added_on": order.created_at, "product_name": product_detail(order.product_id)['product_name'],
                   "shipping_address": shipping_address(order.user_id), "order_status": order.Order_status,
                   "employee_id": order.employee_id}
            res.append(obj)

        employees = Employee.query.all()
        if employees:
            for employee in employees:
                count = Order.query.filter(employee_id=employee.id, order_status="ASSIGNED").count()
                obj1 = {"employee_id": employee.id, "employee_name": employee.name, "order_count": count}
                temp.append(obj1)

        res.append(temp)
        return res
    else:
        return None


@app.route('/admin/orders', methods=['POST'])
@jwt_required
def update_order_status():
    employee_id = request.form.get('employee_id', None)
    order_id = request.form.get('order_id', None)

    if not all((order_id, employee_id)):
        return {"message": "order_id key is required"}, 404
    else:
        order = Order.query.filter_by(id=order_id).first()
        order.order_status = "ASSIGNED"
        order.employee_id = employee_id

        db.session.add(order)
        db.session.commit()

        return {"message": "Employee Assigned successfully"}, 200


@app.route('/admin/orders', methods=['GET'])
@jwt_required
def get_order():
    status = request.args.get('status', None)

    if status == "COMPLETED":
        orders = Order.query.filter_by(order_status="COMPLETED").order_by(desc(Order.created_at)).all()
    elif status == "PENDING":
        orders = Order.query.filter_by(order_status="PENDING").order_by(desc(Order.created_at)).all()
    elif status == "ASSIGNED":
        orders = Order.query.filter_by(order_status="ASSIGNED").order_by(desc(Order.created_at)).all()
    elif status == "REJECT":
        orders = Order.query.filter_by(order_status="REJECT").order_by(desc(Order.created_at)).all()
    else:
        orders = Order.query.order_by(desc(Order.created_at)).all()

    resp = serialization(orders)
    if resp:
        return {"data": resp}, 200
    else:
        return {"message": "No pending order"}, 404
