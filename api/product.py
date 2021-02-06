import os

from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app import app, db
from flask import request
from models.category import Category
from models.product import Product


def get_cat_name(id):
    category = Category.query.filter_by(id=id).first()
    if category:
        return category.name


@app.route('/category', methods=['POST'])
@jwt_required
def add_categories():
    name = request.form.get('name', None)
    description = request.form.get('description', None)
    photo = request.files.get('photo', None)

    if not all((name, description)):
        return {"message": "All fields are required"}, 404

    if photo:
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER_CATEGORY'], photo_filename))
    else:
        photo_filename = None

    category = Category(name=name, description=description, photo=photo_filename)

    db.session.add(category)
    db.session.commit()

    return {"message": "Category added successfully"}, 201


@app.route('/category/<int:id>', methods=['GET'])
def get_categories(id):
    category = Category.query.filter_by(id=id).first()

    if category:
        res = []
        obj = {"name": category.name, "description": category.description, "photo": category.photo, "id": category.id}
        res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No category found"}, 404


@app.route('/category', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()

    if categories:
        res = []
        for category in categories:
            obj = {"name": category.name, "description": category.description, "photo": category.photo, "id": category.id}
            res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No category found"}, 404


@app.route('/category/<int:id>', methods=['DELETE'])
@jwt_required
def delete_category(id):
    if Category.query.filter_by(id=id).delete():
        db.session.commit()
        return {"message": "Category deleted successfully"}, 200
    else:
        return {"message": "No category found for delete"}, 404


@app.route('/product', methods=['POST'])
@jwt_required
def add_product():
    name = request.form.get('name', None)
    description = request.form.get('description', None)
    expirary = request.form.get('expirary', None)
    photo = request.files.get('photo', None)  # yy-mm
    category_id = request.form.get('category_id', None)

    if not all((name, description, category_id, expirary)):
        return {"message": "All fields are required"}, 404

    if photo:
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER_PRODUCT'], photo_filename))
    else:
        photo_filename = None

    product = Product(name=name, description=description, image=photo_filename, category_id=category_id,
                      expiry=expirary)
    db.session.add(product)
    db.session.commit()

    return {"message": "Product added successfully"}, 201


@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.filter_by(id=id).first()

    if product:
        res = []
        obj = {"name": product.name, "product_id": product.id, "description": product.description,
               "photo": product.image, "price": product.price, "category_id": product.category_id}
        res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No product found"}, 404


@app.route('/product/category/<int:id>', methods=['GET'])
def get_product_by_category(id):
    products = Product.query.filter_by(category_id=id).all()

    if products:
        res = []
        for product in products:
            obj = {"product_id": product.id, "name": product.name, "description": product.description,
                   "photo": product.image, "price": product.price, "category_id": product.category_id}
            res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No product found"}, 404


@app.route('/product', methods=['GET'])
def get_product_all():
    products = Product.query.all()

    if products:
        res = []
        for product in products:
            obj = {"name": product.name, "product_id": product.id, "description": product.description,
                   "photo": product.image, "category_id": product.category_id, "price": product.price,
                   "category": get_cat_name(product.category_id)}
            res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No product found"}, 404


@app.route('/product/<int:id>', methods=['DELETE'])
@jwt_required
def delete_product(id):
    if Product.query.filter_by(id=id).delete():
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200
    else:
        return {"message": "No product found for delete"}, 404


@app.route('/allproducts', methods=['GET'])
def get_all_products():
    categories = Category.query.all()
    if categories:
        res = []
        pro_list = []
        for categorie in categories:
            products = Product.query.filter_by(category_id=categorie.id).all()

            if products:
                for product in products:
                    product_obj = {"product_name": product.name, "product_id": product.id,
                                   "price": product.price, "product_description": product.description,
                                   "product_photo": product.image, "category_id": product.category_id}
                    pro_list.append(product_obj)
            else:
                pro_list = []

            obj = {"id": categorie.id, "categorie_name": categorie.name, "description": categorie.description,
                   "photo": categorie.photo, "products": pro_list}
            res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No categories found"}, 404
