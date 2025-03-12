from flask import Flask
from routes import configure_routes
from config import STATIC_FOLDER

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for session management
app.static_folder = STATIC_FOLDER

configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)