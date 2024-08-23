import React, { useRef, useState } from 'react';

function VideoPlayer({ videoSrc }) {
  const videoRef = useRef(null);
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);

  const handleStartRecording = () => {
    setRecording(true);
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks);
          const audioUrl = URL.createObjectURL(audioBlob);
          setAudioURL(audioUrl);
        };

        mediaRecorder.start();

        videoRef.current.addEventListener('ended', () => {
          mediaRecorder.stop();
          setRecording(false);
        });
      })
      .catch(error => console.error('Error accessing microphone:', error));
  };

  return (
    <div>
      <video ref={videoRef} src={videoSrc} controls />
      <button onClick={handleStartRecording} disabled={recording}>
        {recording ? 'Recording...' : 'Start Dubbing'}
      </button>
      {audioURL && <audio src={audioURL} controls />}
    </div>
  );
}

export default VideoPlayer;
