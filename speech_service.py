from pathlib import Path
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
import os
import uuid

# temp directory for audio processing
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def text_to_audio_file(text: str, lang: str = "en") -> str:
    """
    given a text string
    generate an mp3 audio file using google tts
    return the path to the saved file
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")

    filename = f"{uuid.uuid4()}.mp3"
    save_path = TEMP_DIR / filename
    
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(str(save_path))
    
    return str(save_path)

def audio_file_to_text(audio_path: str) -> str:
    """
    given a path to an audio file
    use speech recognition to transcribe content
    return the transcribed text string
    """
    recognizer = sr.Recognizer()
    
    # load audio file
    # supports wav, aiff, flac natively
    # mp3 requires pydub conversion beforehand usually, 
    # but we assume wav for browser microphone uploads
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        
    try:
        # use google web speech api (free tier)
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        raise ConnectionError("API unavailable")

def cleanup_temp_file(file_path: str) -> None:
    """
    given a file path
    remove it from the filesystem if it exists
    """
    path = Path(file_path)
    if path.exists():
        os.remove(path)
