import os
import mysql.connector

# ==============================
# Hàm kết nối MySQL
# ==============================
def connect_db():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQLHOST"),
            user=os.environ.get("MYSQLUSER"),
            password=os.environ.get("MYSQLPASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
            port=int(os.environ.get("MYSQLPORT", 3306))  # Railway cung cấp port
        )
        return connection
    except mysql.connector.Error as e:
        print("DB connection error:", e)
        raise e

# ==============================
# Hàm đăng ký user
# ==============================
def register_user(data):
    try:
        # Validate email phải là @gmail.com
        if not data.get('email', '').endswith('@gmail.com'):
            return {"status": "error", "message": "Email must be a valid @gmail.com address"}

        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s)",
            (data.get('firstName'), data.get('lastName'), data.get('email'), data.get('username'), data.get('password'))
        )
        db.commit()
        cursor.close()
        db.close()
        return {"status": "success", "message": "User registered"}
    except mysql.connector.Error as e:
        print("DB Error:", e)
        return {"status": "error", "message": str(e)}
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}

# ==============================
# Hàm đăng nhập user
# ==============================
def login_user(data):
    try:
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s",
            (data.get('emailOrUsername'), data.get('emailOrUsername'), data.get('password'))
        )
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            return {"status": "success", "user": result}
        else:
            return {"status": "error", "message": "Invalid credentials"}
    except mysql.connector.Error as e:
        print("DB Error:", e)
        return {"status": "error", "message": str(e)}
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}

# ==============================
# Test nhanh (có thể bỏ khi deploy)
# ==============================
if __name__ == "__main__":
    # Thử kết nối database
    try:
        db = connect_db()
        print("Connected to MySQL successfully!")
        db.close()
    except Exception as e:
        print("Failed to connect:", e)
