import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = 'super-secret'
    JWT_TOKEN_LIFETIME = datetime.timedelta(days=365)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://jxedqaolvparjv:5d55f094b1f03a3029506e20172ae8d70cf3bd9e188bd4a372571873da98c3fd@ec2-54-196-1-212.compute-1.amazonaws.com:5432/d9o3tchecsvgpg'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    UPLOAD_FOLDER_CATEGORY = 'uploads/category'
    UPLOAD_FOLDER_PRODUCT = 'uploads/product'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'iamsatyam26@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'xudndaxuwtzextll'
    FLASKY_MAIL_SUBJECT_PREFIX = '[McAfee-Demo]'
    FLASKY_MAIL_SENDER = 'McAfee-Demo Admin <iamsatyam26@gmail.com>'
