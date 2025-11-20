import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def preprocess_image(image):
    """
    Chuẩn hóa ảnh: resize và làm mịn để giảm nhiễu.
    """
    # Resize ảnh về kích thước cố định (256x256)
    image = cv2.resize(image, (256, 256))
    # Làm mịn ảnh bằng Gaussian Blur
    image = cv2.GaussianBlur(image, (5, 5), 0)
    return image

def extract_face_landmarks(image):
    """
    Trích xuất landmarks khuôn mặt từ ảnh sử dụng Mediapipe.
    """
    image = preprocess_image(image)
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.7) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            # Chỉ lấy khuôn mặt đầu tiên
            return results.multi_face_landmarks[0].landmark
        return None

def calculate_landmark_distance(landmarks1, landmarks2):
    """
    Tính toán khoảng cách trung bình giữa các điểm landmarks của hai khuôn mặt.
    """
    distances = []
    for i in range(len(landmarks1)):
        x1, y1, z1 = landmarks1[i].x, landmarks1[i].y, landmarks1[i].z
        x2, y2, z2 = landmarks2[i].x, landmarks2[i].y, landmarks2[i].z
        distances.append(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2))
    return np.mean(distances)

def compare_faces(image1, image2):
    """
    So sánh hai ảnh để xác định khuôn mặt có giống nhau hay không.
    """
    landmarks1 = extract_face_landmarks(image1)
    landmarks2 = extract_face_landmarks(image2)

    if not landmarks1 or not landmarks2:
        return False  # Không phát hiện khuôn mặt trong một hoặc cả hai ảnh

    # Tính toán khoảng cách giữa các điểm landmarks
    avg_distance = calculate_landmark_distance(landmarks1, landmarks2)

    # Điều chỉnh ngưỡng để tăng độ chính xác
    threshold = 0.07  # Giá trị này có thể điều chỉnh (mặc định là 0.05)
    return avg_distance < threshold