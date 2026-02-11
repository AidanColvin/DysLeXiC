import sys
from unittest.mock import MagicMock

# Mock transformers/torch before app import to avoid heavy loads
sys.modules['transformers'] = MagicMock()
sys.modules['torch'] = MagicMock()

import unittest
import json
import base64
from unittest.mock import patch

# Ensure backend is in path
if 'backend' not in sys.path:
    sys.path.append('backend')

# Import the Flask app
from app import app

class TestUIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('suggestion_pipeline.get_robust_suggestions')
    def test_suggest_endpoint(self, mock_suggest):
        mock_suggest.return_value = {
            "status": "success",
            "suggestions": [{"word": "friend", "confidence": "90%"}],
            "ui_adaptations": {}
        }

        # Auth - Default credentials from app.py
        creds = base64.b64encode(b"admin:password").decode("utf-8")
        headers = {'Authorization': f'Basic {creds}', 'Content-Type': 'application/json'}

        payload = {
            "sentence": "hello world",
            "misspelled_word": "worl"
        }

        response = self.app.post('/dyslexia/v2/suggest', headers=headers, data=json.dumps(payload))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(len(response.json['suggestions']), 1)
        self.assertEqual(response.json['suggestions'][0]['word'], 'friend')

    def test_suggest_endpoint_unauthorized(self):
        payload = {
            "sentence": "hello world",
            "misspelled_word": "worl"
        }
        # No auth header
        response = self.app.post('/dyslexia/v2/suggest', json=payload)
        self.assertEqual(response.status_code, 401)

    def test_public_status(self):
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'online')
        self.assertEqual(response.json['mode'], 'Private Secured')

if __name__ == "__main__":
    unittest.main()
