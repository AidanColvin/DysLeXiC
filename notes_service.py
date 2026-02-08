import json
from pathlib import Path
from typing import List, Dict, Any
import time

# simple json storage for user notes
DB_FILE = Path("user_notes.json")

def _load_db() -> Dict[str, Any]:
    """
    internal helper to load the json database
    creates file if it does not exist
    """
    if not DB_FILE.exists():
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_db(data: Dict[str, Any]) -> None:
    """
    internal helper to save data to json database
    """
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_note(url: str, selected_text: str, comment: str) -> Dict[str, Any]:
    """
    given a url, the text selected, and a user comment
    save the note to the database
    returns the created note object
    """
    db = _load_db()
    
    if url not in db:
        db[url] = []
        
    note = {
        "id": int(time.time() * 1000), # simple timestamp id
        "selected_text": selected_text,
        "comment": comment,
        "created_at": time.time()
    }
    
    db[url].append(note)
    _save_db(db)
    return note

def get_notes_for_url(url: str) -> List[Dict[str, Any]]:
    """
    given a url string
    return list of notes associated with that page
    """
    db = _load_db()
    return db.get(url, [])
