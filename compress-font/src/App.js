import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [filePath, setFilePath] = useState('');
  const [savedData, setSavedData] = useState(0);
  const [lostData, setLostData] = useState(0);

  const handleFileUpload = () => {
    const dummyApiResponse = {
      savedData: 500, 
      lostData: 200, 
    };

    setSavedData(dummyApiResponse.savedData);
    setLostData(dummyApiResponse.lostData);
  };

  const handleFilePathChange = (e) => {
    setFilePath(e.target.value);
  };

  return (
    <div className="app">
      <nav className="navbar">
        <div className="navbar-brand">NetCompress</div>
      </nav>
      <div className="container">
        <h1>File Upload and Analysis</h1>
        <div className="file-upload">
          <input
            type="text"
            placeholder="Enter file path..."
            value={filePath}
            onChange={handleFilePathChange}
          />
          <button onClick={handleFileUpload}>Upload File</button>
        </div>
        {savedData > 0 || lostData > 0 ? (
          <div className="analysis-result">
            <h2>Analysis Result</h2>
            <p>Saved Data: {savedData} KB</p>
            <p>Lost Data: {lostData} KB</p>
          </div>
        ) : null}
      </div>
      <footer className="footer">
        <p>SIH2023 Project by Ctrl_Alt_Defeat Team</p>
      </footer>
    </div>
  );
};

export default App;
