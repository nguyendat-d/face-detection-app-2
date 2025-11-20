import React, { useRef, useState } from 'react';
import axios from 'axios';

export default function PersonCard({ person }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [file, setFile] = useState(null);

  const startCamera = () => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play();
        }
      })
      .catch((err) => console.error('Error accessing webcam:', err));
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const handleUploadImage = async () => {
    if (!file) {
      alert('Please upload an image first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:5000/compare', formData);
      alert(`Verification for ${person.name}: ${res.data.status}`);
    } catch (error) {
      console.error('Error verifying face:', error);
    }
  };

  const handleVerifyWithCamera = async () => {
    if (!videoRef.current || !videoRef.current.videoWidth || !videoRef.current.videoHeight) {
      console.error('Video element is not ready or not available.');
      return;
    }

    const canvas = canvasRef.current;
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append('file', blob, 'capture.jpg');

      try {
        const res = await axios.post('http://localhost:5000/compare', formData);
        alert(`Verification for ${person.name}: ${res.data.status}`);
      } catch (error) {
        console.error('Error verifying face:', error);
      }
    }, 'image/jpeg');
  };

  return (
    <div style={{ marginBottom: '20px' }}>
      <p><strong>Name:</strong> {person.name}</p>
      <img
        src={person.image}
        alt={person.name}
        style={{
          width: '200px',
          height: '200px',
          objectFit: 'cover',
          borderRadius: '8px',
          marginTop: '10px',
          border: '1px solid #ddd',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        }}
      />

      {/* Chức năng tải ảnh */}
      <div>
        <label className="file-input">
          Upload Image
          <input
            type="file"
            style={{ display: 'none' }}
            onChange={(e) => setFile(e.target.files[0])}
          />
        </label>
        <button
          className="button button-success"
          onClick={handleUploadImage}
          disabled={!file}
        >
          Verify Image
        </button>
      </div>

      {/* Chức năng bật camera */}
      <div>
        <button className="button button-success" onClick={startCamera}>
          Start Camera
        </button>
        <button className="button button-danger" onClick={stopCamera}>
          Stop Camera
        </button>
        <button
          className="button button-success"
          onClick={handleVerifyWithCamera}
        >
          Verify with Camera
        </button>
      </div>

      <video
        ref={videoRef}
        style={{ width: '100%', maxWidth: '640px', height: 'auto', marginTop: '20px' }}
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}