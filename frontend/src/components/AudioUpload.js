import React, { useState } from 'react';
import axios from 'axios';

function AudioUpload({ onTranscription }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append('audio', file);

    axios.post('http://localhost:5000/upload', formData)
      .then(response => {
        onTranscription(response.data.transcription);
      })
      .catch(error => {
        console.error('Error uploading audio:', error);
      });
  };

  return (
    <div>
      <input type="file" accept="audio/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload Audio</button>
    </div>
  );
}

export default AudioUpload;
