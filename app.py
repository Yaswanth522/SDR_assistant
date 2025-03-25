from flask import Flask
from flask_cors import CORS
from config import load_env_variables
from routes import setup_routes

# Load environment variables
load_env_variables()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register routes
setup_routes(app)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)