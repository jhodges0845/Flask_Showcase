import os

class Config():
    SECRET_KEY = os.environ.get('WEBSITE_KEY')
    SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL'))

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = str(os.environ.get('MAIL_USER'))
    MAIL_PASSWORD = str(os.environ.get('MAIL_PASS'))
