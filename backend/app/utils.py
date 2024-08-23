from moviepy.editor import VideoFileClip, AudioFileClip

def sync_audio_with_video(video_path, audio_path):
    # Load the video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Set the video's audio to the provided audio file
    final_video = video.set_audio(audio)
    output_path = video_path.replace('.mp4', '_dubbed.mp4')  # Save as a new file

    # Write the final video to the output path
    final_video.write_videofile(output_path)
    
    return output_path  # Return the path to the dubbed video
