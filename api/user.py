from flask import request
from flask_jwt_extended import create_access_token
from app import app, db, bcrypt
from models.user import User


@app.route('/user/registration', methods=['POST'])
def user_registration():
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    mobile = request.form.get('mobile', None)

    if not all((name, password, email)):
        return {"message": "All fields are required"}, 404

    user = User.query.filter_by(email=email).first()

    if user:
        return {"message": "Email already exist"}, 404

    password_hash = bcrypt.generate_password_hash(password, 10)
    user = User(name=name, password=password_hash, email=email, mobile=mobile)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id, expires_delta=app.config['JWT_TOKEN_LIFETIME'], fresh=True)
    obj = {"token_type": "Bearer", "access_token": access_token, "name": user.name, "email": user.email,
           "mobile": user.mobile, "user_type": 0}
    return {"data": obj}, 201


@app.route('/user/login', methods=['POST'])
def user_login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if not all((email, password)):
        return {"message": "All fields are required"}, 404

    user = User.query.filter_by(email=email).first()

    if user:
        res = []
        if bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, expires_delta=app.config['JWT_TOKEN_LIFETIME'], fresh=True)
            obj = {"token_type": "Bearer", "access_token": access_token, "name": user.name, "email": user.email,
                   "mobile": user.mobile, "user_type": 0}
            res.append(obj)
            return {"message": res}, 200
        else:
            return {"message": "Invalid password"}, 404
    else:
        return {"message": "No user found"}, 404
