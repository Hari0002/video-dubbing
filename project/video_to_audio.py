from moviepy.editor import VideoFileClip

# Path to the video file
video_path = r"C:\Users\harin\Downloads\Eagles - Hotel California (Live 1977) (Official Video) [HD].mp4"

# Path where the extracted audio will be saved
audio_output_path = r"C:\Users\harin\Downloads\output_audio.mp3"

try:
    # Load the video file
    video = VideoFileClip(video_path)
    
    # Extract and save the audio from the video
    video.audio.write_audiofile(audio_output_path)
    
    print("Audio extracted successfully and saved to:", audio_output_path)
except Exception as e:
    print(f"An error occurred: {e}")
    

