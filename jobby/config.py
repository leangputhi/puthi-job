import psycopg2, os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '7c6b7967-dcba-4796-a261-f36b028144e3' #some random secret key
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') #or "postgresql+psycopg2://postgres:password@localhost/dbname"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1/jobby"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = 'whoosh'
    MAIL_SERVER = "smtp.zoho.com" #configured with zoho, if you use other email provider these settings should be changed
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "your email"
    MAIL_PASSWORD = "password" #your application specific password
