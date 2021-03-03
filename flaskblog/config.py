import os


class Config:
    SECRET_KEY = '7c7797a92c53ab70c22f5db914e49865'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'lampofcheer@gmail.com'
    MAIL_PASSWORD = 'lampofcheer*.exe'
    