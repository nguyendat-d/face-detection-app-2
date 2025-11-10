import React, { useRef, useState } from 'react';
import axios from 'axios';
import './Auth.css'; // Import CSS

export default function WebcamStream() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [result, setResult] = useState(null);

  const startCamera = () => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      })
      .catch((err) => console.error('Error accessing webcam:', err));
  };

  const stopCamera = () => {
    const stream = videoRef.current.srcObject;
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
    }
  };

  const captureImage = async () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageDataUrl = canvas.toDataURL('image/jpeg');
    setCapturedImage(imageDataUrl);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append('file', blob, 'capture.jpg');
      const res = await axios.post('http://localhost:5000/detect', formData);
      setResult(res.data);
    }, 'image/jpeg');
  };

  return (
    <div>
      <h2>Webcam Face Detection</h2>
      <div>
        <button className="button" onClick={startCamera}>
          Start Camera
        </button>
        <button className="button button-danger" onClick={stopCamera}>
          Stop Camera
        </button>
      </div>
      <video ref={videoRef} style={{ width: '100%', maxWidth: '640px', height: 'auto' }} />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <button className="button button-success" onClick={captureImage}>
        Capture Image
      </button>

      {capturedImage && (
        <div>
          <h3>Captured Image</h3>
          <img
            src={capturedImage}
            alt="Captured"
            style={{ width: '100%', maxWidth: '640px', height: 'auto' }}
          />
        </div>
      )}

      {result && (
        <div className="result-container">
          <h3>Detection Info</h3>
          <p>
            <strong>Number of faces detected:</strong> {result.faces}
          </p>
          <p
            className={
              result.faces > 0 ? 'status-success' : 'status-failure'
            }
          >
            <strong>Status:</strong> {result.status}
          </p>
        </div>
      )}
    </div>
  );
}