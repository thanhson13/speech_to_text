import logging
import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

import speech_to_text_service

UPLOAD_FOLDER = 'tmp'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_audio_blob():
    if 'file' not in request.files:
        return jsonify({'success': False})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False})
    audio_channels_count = request.form.get('audio_channel_count')
    if not audio_channels_count:
        return jsonify({'success': False})
    filename = secure_filename(file.filename)
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(full_path)
    result = speech_to_text_service.sample_recognize(
        full_path, int(audio_channels_count))
    return jsonify({'data': result})
