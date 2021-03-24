import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = 'super-secret'
    JWT_TOKEN_LIFETIME = datetime.timedelta(days=365)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://kjvomsfuugmgnr:30baf748b17cadc949d61527c06faa83031275320d4b38b704a2fd8e08e07fdb@ec2-52-44-31-100.compute-1.amazonaws.com:5432/d1ihelegaknn9f'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://postgres:td2u96754w@microsun-ecommerce-database.ccx0fu5sqjsu.us-east-2.rds.amazonaws.com:5432/microsun_ecommerce_database'
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
    S3_BUCKET = 'microsun-ecommerce-bucket'
    S3_KEY = 'AKIAZT4IUTHNCNF5FB4M'
    S3_SECRET = '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'
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    WKHTMLTOPDF_BINARY = 'wkhtmltopdf-pack'
