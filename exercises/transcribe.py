import requests
import os
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = "https://api.sunbird.ai/tasks/org/stt"
ACCESS_TOKEN = os.getenv("AUTH_TOKEN")
# SUPPORTED_FORMATS = ['.wav', '.mp3', '.ogg', '.m4a', '.aac']
SUPPORTED_FORMATS = ['.wav', '.mp3']
MAX_DURATION = 5 * 60 * 1000  # 5 minutes in milliseconds

# Supported languages (API-compatible codes)
SUPPORTED_LANGUAGES = {
    "eng": "English",
    "lug": "Luganda",
    "nyn": "Runyankole",
    "teo": "Ateso",
    "lgg": "Lugbara",
    "ach": "Acholi"
}

def get_audio_duration(audio_path):
    """Return audio duration in milliseconds."""
    try:
        audio = AudioSegment.from_file(audio_path)
        return len(audio)
    except Exception as e:
        print(f"Error reading audio: {str(e)}")
        return None

def convert_audio(input_path, output_format='wav'):
    """Convert audio to API-supported format if needed."""
    try:
        audio = AudioSegment.from_file(input_path)
        filename = f"converted.{output_format}"
        audio.export(filename, format=output_format)
        return filename
    except Exception as e:
        print(f"Conversion failed: {str(e)}")
        return None

def transcribe_audio(audio_path, language):
    """Send audio to Sunbird AI API for transcription."""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    try:
        with open(audio_path, 'rb') as audio_file:
            files = {'audio': (os.path.basename(audio_path), audio_file, 'audio/wav')}
            data = {
                'language': language,
                'adapter': language,
                'recognise_speakers': 'false',
                'whisper': 'false'
            }
            response = requests.post(API_URL, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json().get("audio_transcription", "No transcription found")
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("\n🔊 Sunbird AI Audio Transcriber")
    print(f"Supported languages: {', '.join(SUPPORTED_LANGUAGES.values())}\n")
    
    while True:
        # Get audio file path
        audio_path = input("Please provide path to the audio file (Audio length ≤5 minutes): ").strip(' "\'')
        if audio_path.lower() == 'quit':
            break
        
        # Validate file existence
        if not os.path.exists(audio_path):
            print("Error: File not found. Try again.")
            continue
        
        # Check audio duration
        duration = get_audio_duration(audio_path)
        if duration is None:
            continue
        if duration > MAX_DURATION:
            print(f"Error: Audio is {duration/60000:.1f} minutes (max 5 minutes allowed).")
            continue
        
        # Handle format conversion
        ext = os.path.splitext(audio_path)[1].lower()
        if ext not in SUPPORTED_FORMATS:
            print("Converting to WAV format...")
            converted_path = convert_audio(audio_path)
            if not converted_path:
                continue
            audio_path = converted_path
        
        # Get target language
        print("\nSupported language codes:")
        for code, name in SUPPORTED_LANGUAGES.items():
            print(f"  {code}: {name}")
        
        while True:
            language = input("Choose target language code (e.g., 'lug' for Luganda): ").strip().lower()
            if language in SUPPORTED_LANGUAGES:
                break
            print("Error: Unsupported language. Try again.")
        
        # Transcribe and display
        print("\nTranscribing...")
        transcription = transcribe_audio(audio_path, language)
        
        print(f"\nAudio transcription text in {SUPPORTED_LANGUAGES[language]}:")
        print(transcription)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")