import os

DEV_DB = 'sqlite:///market.db'
pg_user = 'admin'
pg_pass = 'admin'
pg_db = 'market'
pg_host = 'db'
pg_port = 5432
PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'


class Config:
    if os.environ.get('DEBUG') == '1':
        SQLALCHEMY_DATABASE_URI = DEV_DB
    else:
        SQLALCHEMY_DATABASE_URI = PROD_DB
    SECRET_KEY = '812bc484e4d965c184e933e12d79d9f8'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'marioq1717@gmail.com'
    MAIL_PASSWORD = 'testowaniee32!'
