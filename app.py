from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
import os
import logic
import speech_service
import text_service

# initialize flask app
app = Flask(__name__)
# enable cors to allow firefox extension requests
CORS(app)

@app.route("/status", methods=["GET"])
def health_check():
    """
    simple endpoint to verify server is online
    """
    return jsonify({"status": "online", "system": "neuro-read-backend"})

# --- LOGIC ENDPOINTS (Stylometry) ---

@app.route("/analyze/style", methods=["POST"])
def analyze_style():
    """
    endpoint to get stylometric signature
    expects json: {"text": "..."}
    """
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    signature = logic.make_signature(text)
    return jsonify({"signature": signature})

# --- TEXT ENDPOINTS (NLP) ---

@app.route("/nlp/summarize", methods=["POST"])
def summarize():
    """
    endpoint to get key points from text
    expects json: {"text": "..."}
    """
    data = request.get_json()
    text = data.get("text", "")
    summary_points = text_service.summarize_text(text)
    
    return jsonify({
        "original_length": len(text),
        "key_points": summary_points
    })

@app.route("/nlp/correct", methods=["POST"])
def correct():
    """
    endpoint to fix grammar/spelling
    expects json: {"text": "..."}
    """
    data = request.get_json()
    text = data.get("text", "")
    corrected = text_service.correct_grammar(text)
    
    return jsonify({
        "original": text,
        "corrected": corrected,
        "changed": text != corrected
    })

# --- VOICE ENDPOINTS (Audio) ---

@app.route("/voice/speak", methods=["POST"])
def speak():
    """
    endpoint to convert text to speech
    expects json: {"text": "..."}
    returns audio file
    """
    data = request.get_json()
    text = data.get("text", "")
    
    try:
        file_path = speech_service.text_to_audio_file(text)
        # send file to browser, then cleanup is tricky in flask
        # usually handled by a cleanup task or keeping cache
        return send_file(file_path, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/voice/transcribe", methods=["POST"])
def transcribe():
    """
    endpoint to convert audio blob to text
    expects multipart form data with file 'audio'
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
        
    audio_file = request.files['audio']
    filename = f"upload_{audio_file.filename}"
    save_path = Path("temp") / filename
    
    # save upload temporarily
    audio_file.save(save_path)
    
    try:
        # transcribe
        text = speech_service.audio_file_to_text(str(save_path))
        # cleanup
        speech_service.cleanup_temp_file(str(save_path))
        
        return jsonify({"transcription": text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # run on port 5000
    # host 0.0.0.0 is required for container/codespace visibility
    app.run(host="0.0.0.0", port=5000, debug=True)
