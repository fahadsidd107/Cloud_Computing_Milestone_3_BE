import os

# Flask configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

# Database configuration (Google Cloud SQL)
# CLOUD_SQL_USERNAME = os.getenv('CLOUD_SQL_USERNAME', 'clouddb')
# CLOUD_SQL_PASSWORD = os.getenv('CLOUD_SQL_PASSWORD', 'clouddb')
# CLOUD_SQL_DATABASE_NAME = os.getenv('CLOUD_SQL_DATABASE_NAME', 'clouddb')
CLOUD_SQL_USERNAME = 'clouddb'  # Remove os.getenv temporarily for testing
CLOUD_SQL_PASSWORD = 'clouddb'  # Remove os.getenv temporarily for testing
CLOUD_SQL_DATABASE_NAME = 'clouddb' 
CLOUD_SQL_PUBLIC_IP = os.getenv('CLOUD_SQL_PUBLIC_IP', '35.234.93.133')
CLOUD_SQL_CONNECTION_NAME=os.getenv('CLOUD_SQL_CONNECTION_NAME', 'strapi-385510:europe-west3:clouddb')
CLOUD_SQL_PORT = os.getenv('CLOUD_SQL_PORT', '3306')

# Use TCP/IP connection
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@127.0.0.1:3306/{CLOUD_SQL_DATABASE_NAME}'
# SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_PUBLIC_IP}:{CLOUD_SQL_PORT}/{CLOUD_SQL_DATABASE_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# GCS configuration
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME', 'cloudimagesbucket')
GCS_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', 'strapi-385510-04a56795d885.json')
