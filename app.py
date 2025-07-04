from flask import Flask
from routes import configure_routes
from config import STATIC_FOLDER

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.static_folder = STATIC_FOLDER

configure_routes(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)