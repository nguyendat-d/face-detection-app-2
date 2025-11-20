import React, { useRef, useState } from 'react';
import axios from 'axios';
import './Home.css'; // Import CSS file

export default function Home() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [referenceImage, setReferenceImage] = useState(null); // Hình cần so sánh
  const [uploadedFile, setUploadedFile] = useState(null); // Ảnh tải lên
  const [capturedImage, setCapturedImage] = useState(null); // Ảnh được chụp từ camera
  const [verificationResult, setVerificationResult] = useState(null); // Kết quả so sánh

  const startCamera = () => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      })
      .catch((err) => console.error('Không thể truy cập camera:', err));
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

    // Chụp ảnh từ camera
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Hiển thị ảnh đã chụp
    const imageDataUrl = canvas.toDataURL('image/jpeg');
    setCapturedImage(imageDataUrl);

    // Chuyển ảnh thành blob
    return new Promise((resolve) => {
      canvas.toBlob((blob) => resolve(blob), 'image/jpeg');
    });
  };

  const compareFaces = async (source) => {
    if (!referenceImage) {
      alert('Vui lòng tải lên hình cần so sánh trước!');
      return;
    }

    const formData = new FormData();
    formData.append('file1', referenceImage);

    if (source === 'upload') {
      if (!uploadedFile) {
        alert('Vui lòng tải lên ảnh để so sánh!');
        return;
      }
      formData.append('file2', uploadedFile);
    } else if (source === 'camera') {
      const capturedBlob = await captureImage();
      formData.append('file2', capturedBlob, 'capture.jpg');
    }

    try {
      const res = await axios.post('http://localhost:5000/compare_faces', formData);
      setVerificationResult(res.data.status === 'Matched' ? 'Giống' : 'Không giống');
    } catch (error) {
      console.error('Lỗi khi so sánh khuôn mặt:', error);
      setVerificationResult('Lỗi khi thực hiện so sánh');
    }
  };

  return (
    <div className="home-container">
      <h1 className="home-title">So sánh khuôn mặt</h1>

      <div className="section">
        <h2>Hình cần so sánh</h2>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setReferenceImage(e.target.files[0])}
          className="file-input"
        />
        <p className="note">Vui lòng tải hình có 1 khuôn mặt.</p>
        {referenceImage && (
          <img
            src={URL.createObjectURL(referenceImage)}
            alt="Hình cần so sánh"
            className="image-preview"
          />
        )}
      </div>

      <div className="section">
        <h2>Camera</h2>
        <div className="camera-container">
          <video ref={videoRef} className="camera-feed" />
          <canvas ref={canvasRef} style={{ display: 'none' }} />
          {capturedImage && (
            <img
              src={capturedImage}
              alt="Ảnh đã chụp"
              className="image-preview"
            />
          )}
        </div>
        <div className="button-group">
          <button className="button button-success" onClick={startCamera}>
            Bật camera
          </button>
          <button className="button button-danger" onClick={stopCamera}>
            Tắt camera
          </button>
          <button className="button button-primary" onClick={() => compareFaces('camera')}>
            So sánh với ảnh từ camera
          </button>
        </div>
      </div>

      <div className="section">
        <h2>Chức năng tải ảnh</h2>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setUploadedFile(e.target.files[0])}
          className="file-input"
        />
        <button
          className="button button-primary"
          onClick={() => compareFaces('upload')}
          disabled={!uploadedFile}
        >
          So sánh với ảnh tải lên
        </button>
      </div>

      {verificationResult && (
        <div className="result-container">
          <h2>Kết quả</h2>
          <p
            className={`result-text ${
              verificationResult === 'Giống' ? 'success' : 'failure'
            }`}
          >
            {verificationResult}
          </p>
        </div>
      )}
    </div>
  );
}