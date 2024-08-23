import React, { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import VideoPlayer from './components/VideoPlayer';

function App() {
  const [videoSrc, setVideoSrc] = useState('');

  const handleUpload = (data) => {
    setVideoSrc(data.video_url);
  };

  return (
    <div className="App">
      <h1>Video Dubbing Application</h1>
      <VideoUpload onUpload={handleUpload} />
      {videoSrc && <VideoPlayer videoSrc={videoSrc} />}
    </div>
  );
}

export default App;
