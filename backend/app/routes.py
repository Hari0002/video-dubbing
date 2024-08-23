from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.utils import sync_audio_with_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Route to handle video uploads
@app.route('/upload', methods=['POST'])
def upload_video():
    # Check if a video file is provided in the request
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    filename = secure_filename(video.filename)  # Secure the filename
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)  # Save the video to the uploads directory

    return jsonify({'video_url': video_path}), 200  # Return the video path

# Route to handle audio-video syncing
@app.route('/sync', methods=['POST'])
def sync_audio():
    video_path = request.json.get('video_path')
    audio_path = request.json.get('audio_path')

    # Check if both video and audio paths are provided
    if not video_path or not audio_path:
        return jsonify({'error': 'Video or audio path missing'}), 400

    # Use utility function to sync audio with video
    output_url = sync_audio_with_video(video_path, audio_path)
    return jsonify({'output_url': output_url}), 200  # Return the path to the dubbed video

if __name__ == '__main__':
    app.run(debug=True)
