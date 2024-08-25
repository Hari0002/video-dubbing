import speech_recognition as sr
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence

# Load and preprocess the audio
audio_path_mp3 = r"C:\Users\harin\Downloads\example.mp3"
audio_path_wav = r"C:\Users\harin\Downloads\example.wav"

# Convert to wav (16 kHz, mono)
audio = AudioSegment.from_mp3(audio_path_mp3)
audio = audio.set_frame_rate(16000).set_channels(1)
audio = effects.normalize(audio)  # Normalize audio
audio.export(audio_path_wav, format="wav")

audio = AudioSegment.from_wav(audio_path_wav)

# Split audio into chunks
chunks = split_on_silence(audio, min_silence_len=700, silence_thresh=audio.dBFS-16, keep_silence=700)

# Function to transcribe audio chunks and save the output to a text file
def transcribe_audio_chunks(chunks, output_file):
    recognizer = sr.Recognizer()
    full_text = []

    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk{i}.wav"
        chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                try:
                    # Fallback to Sphinx if Google fails
                    text = recognizer.recognize_sphinx(audio_data)
                except sr.UnknownValueError:
                    print(f"Chunk {i}: No recognizer could understand the audio")
                    text = ""
            except sr.RequestError as e:
                print(f"Chunk {i}: Could not request results from Google Web Speech API; {e}")
                text = ""

            full_text.append(text)

    # Join all the chunks into a single transcription
    transcription = " ".join(full_text)

    # Save the transcription to a text file
    with open(output_file, "w") as file:
        file.write(transcription)

    return transcription

# Specify the output text file
output_file = r"C:\Users\harin\Downloads\transcription_output.txt"

# Transcribe chunks and save to text file
transcription = transcribe_audio_chunks(chunks, output_file)

# Print the full transcription
print("Full Transcription:")
print(transcription)
