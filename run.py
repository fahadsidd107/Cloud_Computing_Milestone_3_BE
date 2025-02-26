from dotenv import load_dotenv
from flask_cors import CORS
from sqlalchemy import text
from flask_mail import Mail

# Load environment variables from .env file
load_dotenv()

from app import create_app

app = create_app()
mail = Mail(app)

# Enable CORS for all routes with specific configurations
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",  # Allow all origins (you can restrict this to specific domains in production)
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allowed HTTP methods
            "allow_headers": ["Content-Type", "Authorization"],  # Allowed headers
            "supports_credentials": True,  # Allow cookies and credentials
        }
    }
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

with app.app_context():
    from app import db
    db.session.execute(text('SELECT 1'))  # Test DB connection
    print("Database connection successful!")