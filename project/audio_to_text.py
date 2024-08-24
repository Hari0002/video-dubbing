import speech_recognition as sr
from pydub import AudioSegment

# Paths
audio_path_mp3 = r"C:\Users\harin\Downloads\example.mp3"
audio_path_wav = r"C:\Users\harin\Downloads\example.wav"

# Convert mp3 to wav (16 kHz, mono)
audio = AudioSegment.from_mp3(audio_path_mp3)
audio = audio.set_frame_rate(16000).set_channels(1)
audio.export(audio_path_wav, format="wav")

# Initialize recognizer
recognizer = sr.Recognizer()

try:
    # Load the WAV file
    with sr.AudioFile(audio_path_wav) as source:
        audio_data = recognizer.record(source)
        
        # Recognize the audio
        text = recognizer.recognize_google(audio_data)
        print("Transcription:")
        text = recognizer.recognize_google(audio_data, language="en-US")  # or specify another language code

        print(text)
except sr.UnknownValueError:
    print("Google Web Speech API could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Web Speech API; {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
