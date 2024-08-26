import os
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence
from translate import Translator
import speech_recognition as sr

def extract_audio_from_video(video_path, audio_output_path):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path)
        print("Audio extracted successfully and saved to:", audio_output_path)
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")

def preprocess_audio(audio_path_mp3, audio_path_wav):
    new_var = AudioSegment.from_mp3(audio_path_mp3)
    audio = new_var
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio = effects.normalize(audio)
    audio.export(audio_path_wav, format="wav")
    return audio_path_wav

def split_audio_into_chunks(audio_path_wav):
    audio = AudioSegment.from_wav(audio_path_wav)
    chunks = split_on_silence(audio, min_silence_len=700, silence_thresh=audio.dBFS-16, keep_silence=700)
    return chunks

def transcribe_audio_chunks(chunks):
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
                    text = recognizer.recognize_sphinx(audio_data)
                except sr.UnknownValueError:
                    print(f"Chunk {i}: No recognizer could understand the audio")
                    text = ""
            except sr.RequestError as e:
                print(f"Chunk {i}: Could not request results from Google Web Speech API; {e}")
                text = ""

            full_text.append(text)
        os.remove(chunk_filename)  # Cleanup temporary chunk files

    transcription = " ".join(full_text)
    return transcription

def save_transcription_to_file(transcription, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(transcription)

def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation

def translate_file(input_file_path, output_file_path, target_language):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        translated_text = translate_text(text, target_language)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)

        print(f"Translation to {target_language} completed successfully and saved to {output_file_path}.")
    except Exception as e:
        print(f"An error occurred while translating text: {e}")

def text_to_audio(text, audio_output_path, lang='hi'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(audio_output_path)

        audio = AudioSegment.from_file(audio_output_path)
        audio.export(audio_output_path, format="mp3")

        print(f"Audio file saved successfully at: {audio_output_path}")
    except Exception as e:
        print(f"An error occurred while converting text to audio: {e}")

def combine_audio_with_video(video_path, audio_path, output_video_path):
    try:
        video = VideoFileClip(video_path)
        new_audio = AudioFileClip(audio_path)
        final_video = video.set_audio(new_audio)
        final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
        print(f"Dubbed video saved successfully at: {output_video_path}")
    except Exception as e:
        print(f"An error occurred while combining audio with video: {e}")

# Main workflow with user inputs
if __name__ == "__main__":
    # Prompt user for input paths
    video_path = input("Enter the full path to the video file: ")
    dubbed_video_path = input("Enter the full path where the dubbed video should be saved (including the file name): ")
    target_language = input("Enter the target language code (e.g., 'hi' for Hindi, 'ta' for Tamil, 'ur' for Urdu): ")

    # Derived paths
    extracted_audio_path = os.path.splitext(video_path)[0] + "_extracted_audio.mp3"
    preprocessed_audio_wav_path = os.path.splitext(video_path)[0] + "_audio.wav"
    transcription_file_path = os.path.splitext(video_path)[0] + "_transcription.txt"
    translated_text_file_path = os.path.splitext(video_path)[0] + "_translated.txt"
    translated_audio_path = os.path.splitext(video_path)[0] + "_translated_audio.mp3"

    # Workflow
    extract_audio_from_video(video_path, extracted_audio_path)
    preprocessed_audio_wav_path = preprocess_audio(extracted_audio_path, preprocessed_audio_wav_path)
    chunks = split_audio_into_chunks(preprocessed_audio_wav_path)
    transcription = transcribe_audio_chunks(chunks)
    save_transcription_to_file(transcription, transcription_file_path)
    translate_file(transcription_file_path, translated_text_file_path, target_language)
    with open(translated_text_file_path, 'r', encoding='utf-8') as file:
        translated_text = file.read()
    text_to_audio(translated_text, translated_audio_path, lang=target_language)
    combine_audio_with_video(video_path, translated_audio_path, dubbed_video_path)

    print("Process complete! The dubbed video has been saved.")
