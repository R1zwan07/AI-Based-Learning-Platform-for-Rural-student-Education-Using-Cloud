# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key'
    # Use 'mysql+mysqlconnector' instead of 'mysql+pymysql'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:root@localhost/online_learning'
    SQLALCHEMY_TRACK_MODIFICATIONS = False