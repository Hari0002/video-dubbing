import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import mediainfo

# Specify the paths to ffmpeg and ffprobe
AudioSegment.ffmpeg = "C:\ffmpeg-2024-08-18-git-7e5410eadb-full_build (1)\ffmpeg-2024-08-18-git-7e5410eadb-full_build\doc\ffmpeg.html"
AudioSegment.ffprobe = "C:\ffmpeg-2024-08-18-git-7e5410eadb-full_build (1)\ffmpeg-2024-08-18-git-7e5410eadb-full_build\doc\ffprobe.html"

# Example of using mediainfo to check ffprobe




# Path to the audio file
audio_path = r"C:\Users\hi\Downloads\output_audio.mp3"

# Convert mp3 to wav (SpeechRecognition library works better with wav files)
#audio_wav_path = r"C:\Users\hi\Downloads\output_audio.wav"

# Convert the audio file to wav format
#audio =AudioSegment.from_mp3(audio_path)
#audio.export(audio_wav_path, format="wav")

# Initialize the recognizer
recognizer = sr.Recognizer()

try:
    # Load the audio file
    with sr.AudioFile(audio_path) as source:
        # Record the audio
        audio_data = recognizer.record(source)
        
        # Recognize the audio using Google Web Speech API
        text = recognizer.recognize_google(audio_data)
        
        print("Transcription:")
        print(text)
except sr.UnknownValueError:
    print("Google Web Speech API could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Web Speech API; {e}")
