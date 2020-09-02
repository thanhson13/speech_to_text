import logging
from flask import Flask, render_template, request, jsonify

import speech_to_text_service

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_audio_blob():
    result = speech_to_text_service.sample_recognize(request.data, 2)
    return jsonify({'data': result})
