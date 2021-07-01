import os


class Config:
    DEV_DB = os.environ.get('SQLALCHEMY_DATABASE_URI')

    pg_user = 'admin'
    pg_pass = 'admin'
    pg_db = 'market'
    pg_host = 'localhost'
    pg_port = 5432
    PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
