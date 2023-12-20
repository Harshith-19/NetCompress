import React from 'react'
import './App.css';

export default function Result({props}) {

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text)
          .then(() => {
            alert('Text copied to clipboard:', text);
          })
          .catch((error) => {
            alert('Error copying text:', error);
          });
      };
  return (
    <div>
        <p className='res-head'>Algorithm-{props.algorithm}</p>
        <div className='text-div'>
        <div className="file-paths">
            <div>
            <p className='path-title'><strong>Compressed File Path</strong></p>
            <div className='copy' onClick={() => copyToClipboard(props.compressed_file_path)}>
                <p>{props.compressed_file_path}</p>
            </div>
            </div>

            <div>
            <p className='path-title'><strong>Reconstructed File Path   </strong></p>
            <div className='copy' onClick={() => copyToClipboard(props.reconstructed_file_path)}>
                <p>{props.reconstructed_file_path}</p>
            </div>
            </div>

        </div>

        <p className='path-title'> <strong>Compression ratio: &nbsp;</strong> {props.compression_ratio.toFixed(2)}%,&nbsp;&nbsp;  <strong> Loss Percentage:&nbsp;</strong> {props.loss_percentage.toFixed(2)}%</p>
        </div>
        {/* <div className='pieContainer'>
            <div className='PieChart'>
            <PieChart className= "PieChart" chartData = {fileData} /> 
            </div>
        </div> */}
    </div>
  )
}
