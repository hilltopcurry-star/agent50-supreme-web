import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_complex_secret_key'  # Change in production!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///supreme_delivery.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_secret_key' # Change in production!
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'stripe_secret_key' # Change in production!
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET') or 'stripe_webhook_secret' # Change in production!