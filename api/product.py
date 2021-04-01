import os
import time

import boto3
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app import app, db
from flask import request, send_from_directory
from models.category import Category
from models.product import Product


# local image url format:
# img_url = 'https://microsun-ecommerce-backend.herokuapp.com/static/uploads/product/'
img_url = app.config['S3_LOCATION'] + 'product/'
cat_img_url = app.config['S3_LOCATION'] + 'category/'

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)


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
        photo_name = secure_filename(photo.filename)
        ext = photo_name.rsplit('.', 1)[1].lower()
        photo_name = str(int(time.time())) + "." + ext

        try:
            s3.upload_fileobj(
                photo,
                app.config['S3_BUCKET'],
                'category/' + photo_name,
                ExtraArgs={
                    "ACL": "public-read"
                }
            )

        except Exception as e:
            # This is a catch all exception, edit this part to fit your needs.
            print("Something Happened: ", e)
            return {"message": "Error while uploading to s3"}, 404
    else:
        photo_name = "noimg.jpg"

    category = Category(name=name, description=description, photo=photo_name)

    db.session.add(category)
    db.session.commit()

    return {"message": "Category added successfully"}, 201


@app.route('/category/<int:id>', methods=['GET'])
def get_categories(id):
    category = Category.query.filter_by(id=id).first()

    if category:
        res = []
        obj = {"name": category.name, "description": category.description, "photo": cat_img_url + category.photo,
               "id": category.id}
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
            obj = {"name": category.name, "description": category.description, "photo": cat_img_url + category.photo,
                   "id": category.id}
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
    expirary = '10-00'  # request.form.get('expirary', None)   # yy-mm
    photo = request.files.get('photo', None)
    category_id = request.form.get('category_id', None)
    price = request.form.get('price', None)

    # print(request.form)
    if not all((name, description, category_id, expirary, price)):
        return {"message": "All fields are required"}, 404

    if photo:
        photo_name = secure_filename(photo.filename)
        ext = photo_name.rsplit('.', 1)[1].lower()
        photo_name = str(int(time.time())) + "." + ext

        try:
            s3.upload_fileobj(
                photo,
                app.config['S3_BUCKET'],
                'product/' + photo_name,
                ExtraArgs={
                    "ACL": "public-read"
                }
            )

        except Exception as e:
            # This is a catch all exception, edit this part to fit your needs.
            print("Something Happened: ", e)
            return {"message": "Error while uploading to s3"}, 404
    else:
        photo_name = "noimg.jpg"

    product = Product(name=name, description=description, image=photo_name, category_id=category_id,
                      expiry=expirary, price=price)
    db.session.add(product)
    db.session.commit()

    return {"message": "Product added successfully"}, 201


@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.filter_by(id=id).first()

    if product:
        res = []
        if product.image:
            image = product.image
        else:
            image = "noimage.jpg"

        if product.category_id:
            cat_id = product.category_id
        else:
            cat_id = 1

        obj = {"name": product.name, "product_id": product.id, "description": product.description,
               "photo": img_url + image, "price": product.price, "category_id": cat_id}
        res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No product found"}, 404


# @app.route('/product/category/<int:id>', methods=['GET'])
# def get_product_by_category(id):
#     products = Product.query.filter_by(category_id=id).all()
#
#     if products:
#         res = []
#         for product in products:
#             if product.image:
#                 image = product.image
#             else:
#                 image = "noimage.jpg"
#
#             if product.category_id:
#                 cat_id = product.category_id
#             else:
#                 cat_id = 1
#
#             obj = {"product_id": product.id, "name": product.name, "description": product.description,
#                    "photo": img_url + image, "price": product.price, "category_id": cat_id}
#             res.append(obj)
#         return {"message": res}, 200
#     else:
#         return {"message": "No product found"}, 404


@app.route('/product/category/<int:id>', methods=['GET'])
def get_product_by_category(id):
    products = Product.query.filter_by(category_id=id).all()
    category = Category.query.filter_by(id=id).first()

    if products:
        pro = []
        for product in products:
            if product.image:
                image = product.image
            else:
                image = "noimg.jpg"

            if product.category_id:
                cat_id = product.category_id
            else:
                cat_id = 1

            pro_obj = {"product_id": product.id, "name": product.name, "description": product.description,
                       "photo": img_url + image, "price": product.price, "category_id": cat_id}
            pro.append(pro_obj)

        obj = {"category_id": category.id, "category_name": category.name, "products": pro}

        return {"message": obj}, 200
    else:
        return {"message": "No product found"}, 404


@app.route('/product', methods=['GET'])
def get_product_all():
    products = Product.query.all()

    if products:
        res = []
        for product in products:
            obj = {"name": product.name, "product_id": product.id, "description": product.description,
                   "photo": img_url + product.image, "category_id": product.category_id, "price": product.price,
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
        for categorie in categories:

            products = Product.query.filter_by(category_id=categorie.id).all()

            if products:
                pro_list = []
                for product in products:
                    if product.image:
                        image = product.image
                    else:
                        image = "noimg.jpg"

                    if product.category_id:
                        cat_id = product.category_id
                    else:
                        cat_id = 1

                    product_obj = {"product_name": product.name, "product_id": product.id,
                                   "price": product.price, "product_description": product.description,
                                   "product_photo": img_url + image, "category_id": cat_id}
                    pro_list.append(product_obj)
            else:
                pro_list = []
            obj = {"id": categorie.id, "categorie_name": categorie.name, "description": categorie.description,
                   "photo": categorie.photo, "products": pro_list}
            res.append(obj)
        return {"message": res}, 200
    else:
        return {"message": "No categories found"}, 404


@app.route('/product', methods=['PUT'])
def update_product():
    product_id = request.form.get('product_id', None)
    name = request.form.get('name', None)
    description = request.form.get('description', None)
    price = request.form.get('price', None)

    if Product.query.filter_by(id=product_id).first():
        pro = Product(name=name, description=description, price=price)
        db.session.add(pro)
        db.session.commit()

        return {"message": "Product updated successfully"}, 201
    else:
        return {"message": "No product or invalid product id found"}, 404


@app.route('/static/<path:path>/<string:file>', methods=['GET', 'POST'])
def serve_static_resources(path, file):
    return send_from_directory(path, file)
