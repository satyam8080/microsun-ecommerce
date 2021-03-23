from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from api import user, product, address, admin, cards, cart, order, renewable
from api.emp import orders

from models.user import User
from models.category import Category
from models.product import Product
from models.address import Address
from models.admin import Admin
from models.cards import Card
from models.cart import Cart
from models.order import Order


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
