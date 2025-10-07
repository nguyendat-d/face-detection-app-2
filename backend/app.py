from flask import Flask
from flask_cors import CORS
from routes import auth_bp

app = Flask(__name__)

# ✅ Cho phép tất cả origin (trong dev, bạn có thể thay thành origin cụ thể)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
