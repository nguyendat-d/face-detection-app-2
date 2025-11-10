import React, { useState } from 'react';
import axios from 'axios';
import './Auth.css'; // Import CSS

export default function FaceDetector() {
  const [file, setFile] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [faceInfo, setFaceInfo] = useState(null);

  const upload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:5000/detect_with_boxes', formData, {
        responseType: 'blob',
      });

      const imageUrl = URL.createObjectURL(res.data);
      setResultImage(imageUrl);

      const infoRes = await axios.post('http://localhost:5000/detect', formData);
      setFaceInfo(infoRes.data);
    } catch (error) {
      console.error('Error detecting faces:', error);
    }
  };

  return (
    <div>
      <h2>Upload Image for Face Detection</h2>
      <label className="file-input">
        Choose File
        <input
          type="file"
          style={{ display: 'none' }}
          onChange={(e) => setFile(e.target.files[0])}
        />
      </label>
      <button className="button button-success" onClick={upload} disabled={!file}>
        Detect
      </button>

      {resultImage && (
        <div>
          <h3>Result Image</h3>
          <img
            src={resultImage}
            alt="Detected Faces"
            style={{
              width: '100%',
              maxWidth: '640px',
              height: 'auto',
              border: '1px solid #ddd',
              borderRadius: '8px',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
            }}
          />
        </div>
      )}

      {faceInfo && (
        <div className="result-container">
          <h3>Detection Info</h3>
          <p>
            <strong>Number of faces detected:</strong> {faceInfo.faces}
          </p>
          <p
            className={
              faceInfo.faces > 0 ? 'status-success' : 'status-failure'
            }
          >
            <strong>Status:</strong> {faceInfo.status}
          </p>
        </div>
      )}
    </div>
  );
}