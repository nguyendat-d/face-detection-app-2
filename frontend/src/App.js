import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import FaceDetector from './components/FaceDetector';
import WebcamStream from './components/WebcamStream';
import Home from './components/Home'; // Import Home component
import './App.css';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <Router>
      <div className="app-container">
        {!loggedIn ? (
          <Routes>
            <Route path="/" element={<Login setLoggedIn={setLoggedIn} />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        ) : (
          <div>
            <header className="app-header">
              <h1>Face Detection App</h1>
              <nav className="nav-buttons">
                <Link to="/" className="button">Home</Link>
                <Link to="/upload" className="button button-success">Upload Image</Link>
                <Link to="/webcam" className="button button-danger">Webcam</Link>
                <button className="button" onClick={() => setLoggedIn(false)}>Logout</button>
              </nav>
            </header>
            <main>
              <Routes>
                <Route path="/" element={<Home />} /> {/* Thêm Home */}
                <Route path="/upload" element={<FaceDetector />} />
                <Route path="/webcam" element={<WebcamStream />} />
              </Routes>
            </main>
          </div>
        )}
      </div>
    </Router>
  );
}

export default App;