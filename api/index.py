import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app

# Vercel expects the Flask app to be available as 'app'
if __name__ == "__main__":
    app.run()