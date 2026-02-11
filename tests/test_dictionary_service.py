from unittest.mock import patch, MagicMock
from backend.dictionary_service import fetch_word_details

def test_fetch_word_details_empty_input():
    """Test that empty input returns None."""
    assert fetch_word_details("") is None

def test_fetch_word_details_whitespace_input():
    """Test that whitespace input returns None."""
    assert fetch_word_details("   ") is None

@patch('backend.dictionary_service.requests.get')
def test_fetch_word_details_happy_path(mock_get):
    """Test happy path with mocked API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "word": "example",
        "phonetics": [{"text": "/ɪɡˈzæmpəl/", "audio": "https://api.dictionaryapi.dev/media/pronunciations/en/example-us.mp3"}],
        "meanings": [{
            "partOfSpeech": "noun",
            "definitions": [{"definition": "A representative form or pattern."}]
        }]
    }]
    mock_get.return_value = mock_response

    result = fetch_word_details("example")

    assert result is not None
    assert result["word"] == "example"
    assert result["phonetic"] == "/ɪɡˈzæmpəl/"
    assert result["audio_url"] == "https://api.dictionaryapi.dev/media/pronunciations/en/example-us.mp3"
    assert result["part_of_speech"] == "noun"
    assert result["definition"] == "A representative form or pattern."

@patch('backend.dictionary_service.requests.get')
def test_fetch_word_details_api_error(mock_get):
    """Test API error returns None."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    assert fetch_word_details("unknownword") is None

@patch('backend.dictionary_service.requests.get')
def test_fetch_word_details_exception(mock_get):
    """Test exception handling returns None."""
    mock_get.side_effect = Exception("Connection error")

    assert fetch_word_details("error") is None
