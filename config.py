import os

class Config:
    #make sure to set the secret key in an .env file or change it here to a more secured key
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_password')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    BABEL_DEFAULT_LOCALE = os.getenv('BABEL_DEFAULT_LOCALE', 'en')
    BABEL_DEFAULT_TIMEZONE = os.getenv('BABEL_DEFAULT_TIMEZONE', 'UTC')
    #make sure to set password in an .env file or change it here to a more secured password
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD','AdminPass1!')

class DevelopmentConfig(Config):
    DEBUG = True
    #set the name of your database for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database_dev.db'

class ProductionConfig(Config):
    DEBUG = False
    #set the name of your database for production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///your_database.db')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
