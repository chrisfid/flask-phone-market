import os

DEV_DB = os.environ.get('DEV_DB')
pg_user = os.environ.get('PG_USER')
pg_pass = os.environ.get('PG_PASS')
pg_db = os.environ.get('PG_DB')
pg_host = os.environ.get('PG_HOST')
pg_port = 5432
PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'


class Config:
    if os.environ.get('DEBUG') == '1':
        SQLALCHEMY_DATABASE_URI = DEV_DB
    else:
        SQLALCHEMY_DATABASE_URI = PROD_DB
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
