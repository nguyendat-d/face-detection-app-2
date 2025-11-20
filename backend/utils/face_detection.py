import cv2
import mediapipe as mp
import numpy as np
from flask import jsonify, Response
from PIL import Image

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def detect_faces_with_mediapipe(file, draw_boxes=False):
    image = Image.open(file.stream)
    image_np = np.array(image)

    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

        if results.detections:
            if draw_boxes:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = image_np.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    cv2.rectangle(image_np, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Encode image with boxes to JPEG
                _, buffer = cv2.imencode('.jpg', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
                return Response(buffer.tobytes(), mimetype='image/jpeg')

            return jsonify({"faces": len(results.detections), "status": "Face(s) detected"})
        else:
            return jsonify({"faces": 0, "status": "No face detected"})

def compare_faces_with_mediapipe(image1, image2):
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        # Detect faces in image 1
        results1 = face_detection.process(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        # Detect faces in image 2
        results2 = face_detection.process(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))

        if results1.detections and results2.detections:
            # Compare bounding boxes or other features
            return True  # Assume match
        return False