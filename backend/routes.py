from flask import Blueprint, request, jsonify, Response
from models import register_user, login_user, connect_db
from utils.face_detection import detect_faces_with_mediapipe
from utils.face_comparison import compare_faces, extract_face_landmarks, calculate_landmark_distance
import cv2
import numpy as np

auth_bp = Blueprint('auth', __name__)

# Ảnh mẫu của người cần so sánh (lưu trong thư mục backend)
REFERENCE_IMAGE_PATH = "static/person.jpg"

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    result = register_user(data)
    return jsonify(result)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'emailOrUsername' in data and '@' in data['emailOrUsername']:
        if not data['emailOrUsername'].endswith('@gmail.com'):
            return jsonify({"success": False, "message": "Email must be a valid @gmail.com address"})

    result = login_user(data)
    return jsonify(result)

@auth_bp.route('/detect', methods=['POST'])
def detect():
    file = request.files['file']
    # Giả sử bạn sử dụng OpenCV để phát hiện khuôn mặt
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Trả về danh sách hoặc số lượng khuôn mặt
    return {"faces": len(faces), "status": "Face(s) detected" if len(faces) > 0 else "No face detected"}

@auth_bp.route('/detect_with_boxes', methods=['POST'])
def detect_with_boxes():
    file = request.files['file']
    # Đọc ảnh từ file
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Vẽ khung vuông xung quanh các khuôn mặt
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Chuyển ảnh đã xử lý thành định dạng JPEG
    _, buffer = cv2.imencode('.jpg', image)
    image_bytes = buffer.tobytes()

    # Trả về ảnh đã đóng khung
    return Response(image_bytes, mimetype='image/jpeg')

@auth_bp.route('/webcam_feed', methods=['GET'])
def webcam_feed():
    def generate_frames():
        cap = cv2.VideoCapture(0)  # Mở webcam
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                # Encode frame thành JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@auth_bp.route('/verify', methods=['POST'])
def verify():
    file = request.files['file']
    # Logic kiểm tra khuôn mặt có khớp với dữ liệu đã lưu hay không
    result = detect_faces_with_mediapipe(file)  # Sử dụng hàm đã có
    # Giả sử bạn có logic so sánh khuôn mặt ở đây
    # Trả về kết quả
    return jsonify({"status": "Matched" if result else "Not Matched"})

@auth_bp.route('/compare', methods=['POST'])
def compare():
    file = request.files['file']
    uploaded_image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Đọc ảnh mẫu
    reference_image = cv2.imread(REFERENCE_IMAGE_PATH)

    # So sánh khuôn mặt (giả sử bạn đã có hàm so sánh)
    result = detect_faces_with_mediapipe(file)
    if result:
        # Nếu phát hiện khuôn mặt và khớp
        return jsonify({"status": "Matched"})
    else:
        # Nếu không khớp
        return jsonify({"status": "Not Matched"})

@auth_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    name = request.form['name']
    description = request.form['description']

    # Lưu file vào thư mục static/uploads
    file_path = f"static/uploads/{name}.jpg"
    file.save(file_path)

    # Lưu thông tin vào database (nếu cần)
    # Giả sử bạn có bảng lưu thông tin ảnh
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO images (name, description, file_path) VALUES (%s, %s, %s)",
        (name, description, file_path),
    )
    db.commit()

    return jsonify({"message": "Data uploaded successfully!"})

@auth_bp.route('/compare_faces', methods=['POST'])
def compare_faces_endpoint():
    """
    Endpoint để so sánh hai khuôn mặt từ hai ảnh.
    """
    file1 = request.files.get('file1')  # Hình cần so sánh
    file2 = request.files.get('file2')  # Hình để so sánh

    if not file1 or not file2:
        return jsonify({"status": "error", "message": "Cần cung cấp cả hai hình ảnh"}), 400

    # Decode hình ảnh
    image1 = cv2.imdecode(np.frombuffer(file1.read(), np.uint8), cv2.IMREAD_COLOR)
    image2 = cv2.imdecode(np.frombuffer(file2.read(), np.uint8), cv2.IMREAD_COLOR)

    # So sánh khuôn mặt
    match = compare_faces(image1, image2)

    if match:
        return jsonify({"status": "Matched", "message": "Hai khuôn mặt giống nhau"})
    else:
        return jsonify({"status": "Not Matched", "message": "Hai khuôn mặt không giống nhau"})