import React, { useState } from 'react';
import AudioUpload from './components/AudioUpload';
import TranscriptionDisplay from './components/TranscriptionDisplay';

function App() {
  const [transcription, setTranscription] = useState('');

  return (
    <div className="App">
      <h1>Audio to Text Translation</h1>
      <AudioUpload onTranscription={setTranscription} />
      <TranscriptionDisplay transcription={transcription} />
    </div>
  );
}

export default App;
