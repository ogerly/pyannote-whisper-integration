import torch
from pyannote.audio import Pipeline, Model
from dotenv import load_dotenv
import os
from pydub import AudioSegment
import whisper
from flask import Flask, request, render_template, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
import time
import json

# Flask App Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav'}

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Initialize Whisper Model
print("[INFO] Lade Whisper-Modell...")
whisper_model = whisper.load_model("base")
print("[INFO] Whisper-Modell erfolgreich geladen.")

# Initialize PyAnnote Pipeline
pipeline = None
if HUGGINGFACE_API_KEY:
    try:
        print("[INFO] Initialisiere pyannote Pipeline...")
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=HUGGINGFACE_API_KEY)
        if torch.cuda.is_available():
            pipeline.to(torch.device("cuda"))
            print("[INFO] Pipeline zur GPU gesendet.")
        else:
            print("[WARNUNG] Keine GPU gefunden. Verwende CPU.")
    except Exception as e:
        print(f"[ERROR] Fehler beim Laden der pyannote Pipeline: {e}")
        print("[HINWEIS] Besuche https://huggingface.co/pyannote/speaker-diarization-3.1 und akzeptiere die Nutzungsbedingungen, falls notwendig.")
else:
    print("[ERROR] Kein HuggingFace API-Schlüssel gefunden. Bitte sicherstellen, dass die .env Datei korrekt ist.")

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index2.html')

# Static route for serving uploaded files
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return jsonify({"error": "Keine Datei hochgeladen"}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "Keine Datei ausgewählt"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Ungültiger Dateityp"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print(f"[INFO] Datei gespeichert unter: {filepath}")

    # Convert to WAV if needed
    if filepath.endswith('.mp3'):
        try:
            print("[INFO] Konvertiere MP3-Datei nach WAV...")
            audio = AudioSegment.from_file(filepath, format="mp3")
            wav_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{os.path.splitext(filename)[0]}.wav")
            audio.export(wav_filepath, format="wav")
            print(f"[INFO] Konvertierung abgeschlossen. WAV-Datei gespeichert unter: {wav_filepath}")
        except Exception as e:
            return jsonify({"error": f"Fehler bei der Konvertierung: {e}"}), 500
    else:
        wav_filepath = filepath

    # Enable analyze button after successful upload
    return jsonify({"message": "Datei erfolgreich hochgeladen", "wav_filepath": wav_filepath})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    wav_filepath = data.get('wav_filepath')

    if not wav_filepath or not os.path.exists(wav_filepath):
        print(f"[ERROR] Audiodatei nicht gefunden: {wav_filepath}")
        return jsonify({"error": "Audiodatei nicht gefunden"}), 400

    if pipeline is None:
        print("[ERROR] Die pyannote Pipeline wurde nicht initialisiert.")
        return jsonify({"error": "Die pyannote Pipeline wurde nicht initialisiert."}), 500

    try:
        print(f"[INFO] Starte Diarisierung für Datei: {wav_filepath}")
        diarization = pipeline(wav_filepath)
        print("[INFO] Diarisierung erfolgreich abgeschlossen.")

        # Transkription und Segmentzuordnung
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start = int(turn.start * 1000)  # in Millisekunden
            end = int(turn.end * 1000)      # in Millisekunden
            try:
                segment_audio = AudioSegment.from_file(wav_filepath)[start:end]
                segment_path = f"./uploads/temp_segment_{speaker}_{start}_{end}.wav"
                segment_audio.export(segment_path, format="wav")
            except Exception as e:
                print(f"[ERROR] Fehler beim Erstellen des Segment-Audiofiles: {e}")
                continue

            # Transkribiere das jeweilige Segment mit Whisper
            print(f"[INFO] Starte Transkription des Segments: {segment_path}")
            try:
                segment_result = whisper_model.transcribe(segment_path)
                segment_transcript = segment_result['text']
                print(f"[INFO] Transkription abgeschlossen: {segment_transcript}")
            except Exception as e:
                print(f"[ERROR] Fehler bei der Transkription des Segments: {e}")
                continue

            # Speichern der Segmente und Transkripte
            segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker,
                "transcript": segment_transcript
            })

            # Lösche temporäre Datei
            try:
                os.remove(segment_path)
            except Exception as e:
                print(f"[WARNUNG] Fehler beim Löschen der temporären Datei {segment_path}: {e}")

        # Rückgabe der Analyseergebnisse
        print("[INFO] Analyse erfolgreich abgeschlossen.")
        return jsonify({"segments": segments})
    except Exception as e:
        print(f"[ERROR] Fehler bei der Diarisierung oder Transkription: {e}")
        return jsonify({"error": f"Fehler bei der Diarisierung oder Transkription: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
