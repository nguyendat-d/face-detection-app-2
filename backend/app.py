from flask import Flask
from flask_cors import CORS
from routes import auth_bp

app = Flask(__name__)

# ✅ Cho phép tất cả origin (trong dev, bạn có thể thay thành origin cụ thể)
CORS(app, resources={r"/*": {"origins": "http://localhost:3001"}})

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
    
# filepath: f:\cac du an\face-detection-app - Copy\backend\app.py
import os
# ...existing code...
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)