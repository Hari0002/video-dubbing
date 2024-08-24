from gtts import gTTS
from pydub import AudioSegment

def text_to_audio(text, audio_output_path, lang='hi'):
    try:
        # Convert text to speech using gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(audio_output_path)
        
        # Optionally, use pydub to load and manipulate the audio file
        audio = AudioSegment.from_file(audio_output_path)
        audio.export(audio_output_path, format="mp3")
        
        print(f"Audio file saved successfully at: {audio_output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_translated_text_file_to_audio(input_file_path, output_audio_path, lang='hi'):
    try:
        # Read the content of the translated text file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Convert the translated text to audio
        text_to_audio(text, output_audio_path, lang)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file_path = r"C:\Users\hi\Downloads\output_text_urdu.txt"
output_audio_path = r"C:\Users\hi\Downloads\output_audio.mp3"

# Convert translated text file to audio
convert_translated_text_file_to_audio(input_file_path, output_audio_path, lang='hi')  # 'hi' for Hindi, adjust as needed
