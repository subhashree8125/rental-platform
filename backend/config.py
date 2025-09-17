import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "broklink_secret")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Hari%405502@localhost:3306/broklink"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed image formats