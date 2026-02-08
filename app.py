import os
import logging
from functools import wraps
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import base64

# Import your robust modules
import suggestion_pipeline
import readability_service
import structure_analyzer

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeuroRead-Secure")

app = Flask(__name__)

# CORS: Allow all origins (Extension needs this)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- SECURITY CONFIGURATION ---
# Get credentials from Environment Variables (Set these in Render/Codespace!)
# Default to "admin"/"password" ONLY if not set (Safe fallback for dev)
AUTH_USER = os.environ.get("APP_USER", "admin")
AUTH_PASS = os.environ.get("APP_PASS", "password")

def check_auth(username, password):
    """Checks if provided credentials match environment variables."""
    return username == AUTH_USER and password == AUTH_PASS

def authenticate():
    """Sends a 401 response that enables basic auth."""
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def requires_auth(f):
    """
    Decorator to require Authentication for specific routes.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response

# --- SECURED ENDPOINTS ---

@app.route("/status", methods=["GET"])
# We leave status public so you can check if server is alive without logging in
def status():
    return jsonify({
        "status": "online", 
        "mode": "Private Secured",
        "auth_enabled": True
    })

@app.route("/dyslexia/v2/suggest", methods=["POST"])
@requires_auth  # <--- LOCKED
def suggest_secure():
    """
    Private Spellcheck. 
    Only runs if the Extension sends correct Username/Password.
    """
    try:
        data = request.get_json()
        sentence = data.get("sentence", "")
        misspelled = data.get("misspelled_word", "").lower()
        
        # Load vocab (In production, load globally)
        from nltk.corpus import words as nltk_words
        english_vocab = [w.lower() for w in nltk_words.words() if len(w) > 2]

        # Use the Authenticated Username as the Profile ID
        # This ensures the model learns specifically from THIS user.
        user_id = request.authorization.username

        result = suggestion_pipeline.get_robust_suggestions(
            sentence, misspelled, english_vocab, user_id=user_id 
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/dyslexia/feedback", methods=["POST"])
@requires_auth  # <--- LOCKED
def feedback_secure():
    """Private Learning Endpoint"""
    data = request.get_json()
    user_id = request.authorization.username
    
    suggestion_pipeline.handle_user_feedback(
        data.get("misspelling"), data.get("chosen"), data.get("action"), user_id=user_id
    )
    return jsonify({"status": "learned"})

@app.route("/view/reader-mode", methods=["POST"])
@requires_auth  # <--- LOCKED
def reader_mode_secure():
    data = request.get_json()
    result = readability_service.fetch_and_clean_url(data.get("url"))
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
