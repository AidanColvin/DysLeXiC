import requests
from typing import Dict, Any, Optional

# using free dictionary api
API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"

def fetch_word_details(word: str) -> Optional[Dict[str, Any]]:
    """
    given a word string
    return a dictionary containing definition, phonetics, and audio url
    fetches from external dictionary api
    """
    clean_word = word.strip().lower()
    if not clean_word:
        return None
        
    try:
        response = requests.get(API_URL.format(clean_word))
        if response.status_code != 200:
            return None
            
        data = response.json()[0]
        
        # extract first valid audio link
        audio_url = ""
        phonetic_text = data.get("phonetic", "")
        
        for p in data.get("phonetics", []):
            if p.get("audio"):
                audio_url = p["audio"]
                if not phonetic_text and p.get("text"):
                    phonetic_text = p["text"]
                break
        
        # extract first definition
        definition = "No definition found."
        part_of_speech = "unknown"
        
        if data.get("meanings"):
            meaning = data["meanings"][0]
            part_of_speech = meaning.get("partOfSpeech", "unknown")
            if meaning.get("definitions"):
                definition = meaning["definitions"][0].get("definition", "")

        return {
            "word": data.get("word", clean_word),
            "phonetic": phonetic_text,
            "audio_url": audio_url,
            "part_of_speech": part_of_speech,
            "definition": definition
        }
        
    except Exception:
        return None
