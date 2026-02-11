import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the Flask app
from app import app

# Vercel expects the app to be available directly
# Export the Flask app instance
application = app

# For local testing
if __name__ == "__main__":
    app.run(debug=True)