from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import logging


def sample_recognize(blob, num_audio_channels=1):
    """
    Transcribe a short audio file using synchronous speech recognition
    """

    client = speech_v1.SpeechClient()

    # The language of the supplied audio
    language_code = "vi-VN"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "audio_channel_count": num_audio_channels,
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    audio = {"content": blob}

    response = client.recognize(config, audio)
    logging.debug(response)
    final_result = []
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        final_result = {'transcript': alternative.transcript}
    return final_result
