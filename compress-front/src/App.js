import React, { useState, useEffect } from 'react';
// import { useEffect, useState } from 'react';
import PieChart from './PieChart'
import './App.css';
import Result from './Result';
const App = () => {

  const dummy = [
    {
      'algorithm': 'H.264',
      'compressed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/compressed_H.264.mp4',
      'reconstructed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/reconstructed_H.264.mp4',
      'compression_ratio': 5.194300252432517,
      'loss_percentage': 0.5142844950140889
    },
    {
      'algorithm': 'H.265',
      'compressed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/compressed_H.265.mp4',
      'reconstructed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/reconstructed_H.265.mp4',
      'compression_ratio': 10.605475584136613,
      'loss_percentage': 0.533040896190122
    },
    {
      'algorithm': 'H.264',
      'compressed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/compressed_H.264.mp4',
      'reconstructed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/reconstructed_H.264.mp4',
      'compression_ratio': 5.194300252432517,
      'loss_percentage': 0.5142844950140889
    },
    {
      'algorithm': 'H.265',
      'compressed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/compressed_H.265.mp4',
      'reconstructed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/reconstructed_H.265.mp4',
      'compression_ratio': 10.605475584136613,
      'loss_percentage': 0.533040896190122
    },
    {
      'algorithm': 'H.264',
      'compressed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/compressed_H.264.mp4',
      'reconstructed_file_path': '/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/reconstructed_H.264.mp4',
      'compression_ratio': 5.194300252432517,
      'loss_percentage': 0.5142844950140889
    },
   
  ];
  const [loading, setLoading] = useState(false);
  const [op, setOp] = useState([]);
  const [filePath, setFilePath] = useState('');
  const [savedData, setSavedData] = useState(0);
  const [lostData, setLostData] = useState(0);
  const [fileType, setFileType] = useState('');
  const [compressedFilePath, setCompressedFilePath] = useState('/mnt/c/Users/homep/Desktop/SIH/NetCompress/Compression/compressed_H.264.mp4');
  const [reconstructedFilePath, setReconstructedFilePath] = useState('/mnt/c/Users/homep/Desktop/SIH/NetCompress/res/res.264.mp4');
  useEffect(() => {
    const compressionRatios = op.map(item => item.compression_ratio.toFixed(2));
    const lossPercentage = op.map(item => item.loss_percentage.toFixed(2));
    const algos = op.map(item => item.algorithm);
  
    setRatioGraph({
      labels: algos,
      datasets: [
        {
          label: 'Compression ratio',
          data: compressionRatios,
          backgroundColor: ['#6e88fa'],
          borderColor: '#6e88fa',
          borderWidth: 1.3,
          tension: 0.1,
          fill: false,
        },
      ],
    });
  
    setLossGraph({
      labels: algos,
      datasets: [
        {
          label: 'Loss Percentage',
          data: lossPercentage,
          backgroundColor: ['#b06400'],
          borderColor: '#b06400',
          borderWidth: 1.3,
          tension: 0.1,
          fill: false,
        },
      ],
    });
  }, [op]);
  const compressionRatios = op.map(item => item.compression_ratio.toFixed(2));
  const lossPercentage = op.map(item => item.loss_percentage.toFixed(2));
  const algos = op.map(item => item.algorithm);
  const [ratioGraph, setRatioGraph] = useState({
    labels: algos,
    datasets: [
      {
        label: 'Compression ratio',
        data: compressionRatios,
        backgroundColor: [      '#6e88fa'],
        borderColor: '#6e88fa',
        borderWidth: 1.3,
        tension:0.1,
        fill: false,
      },
    ],
  });
  // useEffect(() => {
  //   setRatioGraph((prevFileData) => ({
  //     ...prevFileData,
  //     datasets: [
  //       {
  //         ...prevFileData.datasets[0],
  //         data: [compression_ratio, loss_percentage],
  //       },
  //     ],
  //   }));
  // }, [compression_ratio, loss_percentage]);

  const [lossGraph, setLossGraph] = useState({
    labels: algos,
    datasets: [
      {
        label: 'Loss Percentage',
        data: lossPercentage,
        backgroundColor: [      '#b06400'],
        borderColor: '#b06400',
        borderWidth: 1.3,
        tension:0.1,
        fill: false,
      },
    ],
  });
  // useEffect(() => {
  //   setRatioGraph((prevFileData) => ({
  //     ...prevFileData,
  //     datasets: [
  //       {
  //         ...prevFileData.datasets[0],
  //         data: [compression_ratio, loss_percentage],
  //       },
  //     ],
  //   }));
  // }, [compression_ratio, loss_percentage]);

  const getFileTypeFromExtension = (extension) => {
    const extensionMap = {
      txt: 'Text',
      jpg: 'Image',
      jpeg: 'Image',
      png: 'Image',
      gif: 'Image',
      mp3: 'Audio',
      wav: 'Audio',
      mp4: 'Video',
      mov: 'Video',
      
    };
  
    const fileType = extensionMap[extension.toLowerCase()];
    return fileType || 'Others';
  };
  // const [formData, setFormData] = useState({
  //   file_path: '',
  //   file_type: '',
  // });
  // useEffect(() => {
  //   setFormData({
  //     file_path: filePath,
  //     file_type: fileType,
  //   });
  // }, [filePath, fileType]);  
  const handleCompressedFilePathChange = (e) => {
    setCompressedFilePath(e.target.value);
  };

  const handleReconstructedFilePathChange = (e) => {
    setReconstructedFilePath(e.target.value);
  };

  // const handleFileUpload = () => {

  //   const dummyApiResponse = {
  //     savedData: 500,
  //     lostData: 200,
  //   };
  //   const fileExtension = filePath.split('.').pop();
  //   const detectedFileType = getFileTypeFromExtension(fileExtension);
  //   setFileType(detectedFileType);
  //   setSavedData(dummyApiResponse.savedData);
  //   setLostData(dummyApiResponse.lostData);

  //   const formData = {
  //     "file_path":filePath,
  //     "file_type":fileType,
  //   };
  //   console.log('Data being sent to backend:', formData);

  //   fetch('http://127.0.0.1:8000/upload/', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify(formData),
  //   })
  //     .then(response => response.json()) 
  //     .then(data => {
  //       setOp(data); 
  //     })
  //     .catch(error => {

  //       console.error('Error:', error);
  //     });
  // };

  const handleFilePathChange = (e) => {
    setFilePath(e.target.value);
  };

  const handleFileTypeChange = (e) => {
    setFileType(e.target.value);
  };


  const [formData, setFormData] = useState({
    "filePath": '',
    "fileType": '',
  });
  
  useEffect(() => {
    const fileExtension = filePath.split('.').pop();
    const detectedFileType = getFileTypeFromExtension(fileExtension);
    setFileType(detectedFileType);
  }, [filePath]);
  
  useEffect(() => {
    setFormData({
      "filePath": filePath,
      "fileType": fileType,
    });
  }, [filePath, fileType]);
  
  const handleFileUpload = () => {
    setLoading(true);
    const dummyApiResponse = {
      savedData: 500,
      lostData: 200,
    };
    setSavedData(dummyApiResponse.savedData);
    setLostData(dummyApiResponse.lostData);
  
    console.log('Data being sent to backend:', formData);
  
    fetch('http://127.0.0.1:8000/upload/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then(response => response.json()) 
      .then(data => {
        setOp(data); 
        setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setLoading(false);
      });
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
          
          <button onClick={handleFileUpload}>Upload</button>
        </div>
        {savedData > 0 || lostData > 0 ? (
          <div>
            {loading ? 
                  <div className="loader-container">
                  <div className='loader'></div>
                </div>: 
          
            <div className="analysis-result">
              <h2>Analysis Result</h2>

              <div className='charts'> 
            
                {op.map((currentValue, index) => (
                  <div key={index}>
                    <Result props={currentValue} />
                  </div>
                ))}
                
              </div>
                  <div className='graph-bg'>
                    <div className='res-head'><p><strong>Compression and Loss for each Algorithm</strong></p></div>
                    <div className='graphs'>
                          <div className='pieContainer'>
                            <div className='PieChart'>
                            <PieChart className= "PieChart" chartData = {ratioGraph} /> 
                            </div>
                          </div>
                          <div className='pieContainer'>
                              <div className='PieChart'>
                              <PieChart className= "PieChart" chartData = {lossGraph} /> 
                              </div>
                          </div>
                    </div>
                  </div>
            </div>
            }
          </div>

        ) : 
        <div className="">
          <h2>Results will appear Below</h2>
        </div>
      }
      </div>
      
      <footer className="footer">
        <p>SIH2023 Project by Ctrl_Alt_Defeat Team</p>
      </footer>
    </div>
  );
};

export default App;
