from flask import Flask, render_template, request
from gtts import gTTS
import base64
import io
from langdetect import detect

app = Flask(__name__)

def generate_audio(language, text):
    # Create a gTTS object based on the selected language and input text
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the speech to a temporary file and read the file contents as bytes
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    audio_data = audio_file.read()

    # Encode audio data as base64
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    return audio_base64

def detect_language(text):
    try:
        language_code = detect(text)
        return language_code
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_base64 = None
    if request.method == 'POST':
        text = request.form['text']
        language_code = detect_language(text)
        if language_code is None:
            return render_template('index.html', error='Unable to detect language!')
        
        audio_base64 = generate_audio(language_code, text)

    return render_template('index.html', audio_base64=audio_base64)

if __name__ == '__main__':
    app.run(debug=True)
