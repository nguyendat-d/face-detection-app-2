from flask import Flask
from flask_cors import CORS
from routes import auth_bp
import os

app = Flask(__name__)

# ✅ Cho phép tất cả origin (khi deploy thực tế, bạn có thể thay localhost bằng domain thật)
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Đăng ký blueprint
app.register_blueprint(auth_bp)

# ✅ Cấu hình chạy Flask đúng trên Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
