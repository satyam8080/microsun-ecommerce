from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import desc

from app import app, bcrypt, db
from flask import request

from models.address import Address
from models.employee import Employee
from models.order import Order
from models.product import Product


def shipping_address(user_id):
    address = Address.query.filter_by(user_id=user_id).order_by(desc(Address.created_at)).first()
    if address:
        return address.address
    else:
        return None


def product_detail(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        obj = {"product_name": product.name}
        return obj
    else:
        return None


def assigned(emp_id):
    return Order.query.filter(Order.employee_id == emp_id, Order.status == "ASSIGNED").count()


def pending(emp_id):
    return Order.query.filter(Order.employee_id == emp_id, Order.status == "PENDING").count()


@app.route('/employee/registration', methods=['POST'])
def employee_registration():
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    mobile = request.form.get('mobile', None)

    if not all((name, password, email)):
        return {"message": "All fields are required"}, 404

    employee = Employee.query.filter_by(email=email).first()

    if employee:
        return {"message": "Email already exist"}, 404

    password_hash = bcrypt.generate_password_hash(password, 10)
    employee = Employee(name=name, password=password_hash, email=email, mobile=mobile)
    db.session.add(employee)
    db.session.commit()

    access_token = create_access_token(identity=employee.id, fresh=True)
    obj = {"token_type": "Bearer", "access_token": access_token, "name": employee.name, "email": employee.email,
           "mobile": employee.mobile, "user_type": 2, "id": employee.id}
    return {"data": obj}, 201


@app.route('/employee/login', methods=['POST'])
def employee_login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if not all((email, password)):
        return {"message": "All fields are required"}, 404

    employee = Employee.query.filter_by(email=email).first()

    if employee:
        res = []
        if bcrypt.check_password_hash(employee.password, password):
            access_token = create_access_token(identity=employee.id, fresh=True)
            obj = {"token_type": "Bearer", "access_token": access_token, "name": employee.name, "email": employee.email,
                   "mobile": employee.mobile, "user_type": 2, "id": employee.id}
            res.append(obj)
            return {"message": res}, 200
        else:
            return {"message": "Invalid password"}, 404
    else:
        return {"message": "No employee found"}, 404


@app.route('/employee/orders', methods=['GET'])
@jwt_required
def employee_orders_get():
    employee_id = get_jwt_identity()
    orders = Order.query.filter_by(employee_id=employee_id).order_by(desc(Order.created_at)).all()

    if orders:
        res = []
        for order in orders:
            obj = {"id": order.id, "user_id": order.user_id, "product_id": order.product_id, "price": order.price,
                   "transaction_id": order.transaction_id, "mode": order.mode, "status": order.status,
                   "added_on": order.created_at, "product_name": product_detail(order.product_id)['product_name'],
                   "shipping_address": shipping_address(order.user_id), "order_status": order.Order_status,
                   "employee_id": order.employee_id, "updated_at": order.updated_at}
            res.append(obj)
        return {"data": res}, 200
    else:
        return {"message": "No order history"}, 404


@app.route('/employee/orders', methods=['POST'])
@jwt_required
def update_employee_order_status():
    employee_id = get_jwt_identity()
    order_id = request.form.get('order_id', None)
    status = request.form.get('status', None)

    if not all((order_id, status)):
        return {"message": "order_id key is required"}, 404
    else:
        order = Order.query.filter_by(id=order_id).first()
        order.order_status = status
        order.employee_id = employee_id

        db.session.add(order)
        db.session.commit()

        res = {"id": order.id, "user_id": order.user_id, "product_id": order.product_id, "price": order.price,
               "transaction_id": order.transaction_id, "mode": order.mode, "status": order.status,
               "added_on": order.created_at, "product_name": product_detail(order.product_id)['product_name'],
               "shipping_address": shipping_address(order.user_id), "order_status": order.Order_status,
               "employee_id": order.employee_id, "updated_at": order.updated_at}

        return {"data": res}, 200


@app.route('/employee/<int:id>', methods=['DELETE'])
@jwt_required
def delete_employee(id):
    if Employee.query.filter_by(id=id).delete():
        return {"message": "Employee deleted "}, 200
    else:
        return {"message": "Employee cant deleted"}, 404


@app.route('/employee', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    if employees:
        res = []
        for employee in employees:
            obj = {"name": employee.name, "email": employee.email, "pending_tasks": pending(employee.id),
                   "assigned_task": assigned(employee.id), "mobile": employee.mobile, "user_type": 2,
                   "id": employee.id}
            res.append(obj)
        return {"data": res}, 200
    else:
        return {"message": "No employee registered yet"}, 404
