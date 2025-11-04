import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="thanhdat12345",
        database="face_auth"
    )

def register_user(data):
    try:
        if not data['email'].endswith('@gmail.com'):
            return {"status": "error", "message": "Email must be a valid @gmail.com address"}

        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, username, password) VALUES (%s, %s, %s, %s, %s)",
            (data['firstName'], data['lastName'], data['email'], data['username'], data['password']),
        )
        db.commit()
        return {"message": "User registered"}
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "message": str(e)}

def login_user(data):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s",
        (data['emailOrUsername'], data['emailOrUsername'], data['password']),
    )
    result = cursor.fetchone()
    return {"success": bool(result)}

import os
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "thanhdat12345"),
        database=os.environ.get("DB_NAME", "face_auth")
    )
