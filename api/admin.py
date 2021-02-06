from flask_jwt_extended import create_access_token

from app import app, bcrypt, db
from flask import request
from models.admin import Admin


@app.route('/admin/registration', methods=['POST'])
def admin_registration():
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    mobile = request.form.get('mobile', None)

    if not all((name, password, email)):
        return {"message": "All fields are required"}, 404

    admin = Admin.query.filter_by(email=email).first()

    if admin:
        return {"message": "Email already exist"}, 404

    password_hash = bcrypt.generate_password_hash(password, 10)
    admin = Admin(name=name, password=password_hash, email=email, mobile=mobile)
    db.session.add(admin)
    db.session.commit()

    res = []
    access_token = create_access_token(identity=admin.id, fresh=True)
    obj = {"token_type": "Bearer", "access_token": access_token, "name": admin.name, "email": admin.email,
           "mobile": admin.mobile, "user_type": 1, "id": admin.id}
    res.append(obj)
    return {"message": res}, 201


@app.route('/admin/login', methods=['POST'])
def admin_login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if not all((email, password)):
        return {"message": "All fields are required"}, 404

    admin = Admin.query.filter_by(email=email).first()

    if admin:
        res = []
        if bcrypt.check_password_hash(admin.password, password):
            access_token = create_access_token(identity=admin.id, expires_delta=app.config['JWT_TOKEN_LIFETIME'], fresh=True)
            obj = {"token_type": "Bearer", "access_token": access_token, "name": admin.name, "email": admin.email, 
                   "mobile": admin.mobile, "user_type": 1, "id": admin.id}
            res.append(obj)
            return {"message": res}, 200
        else:
            return {"message": "Invalid password"}, 404
    else:
        return {"message": "No admin found"}, 404
