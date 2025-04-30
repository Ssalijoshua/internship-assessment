import requests
import json

# Configuration
API_URL = "https://api.sunbird.ai/tasks/nllb_translate"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXRyaWNrY21kIiwiYWNjb3VudF90eXBlIjoiRnJlZSIsImV4cCI6NDg2OTE4NjUzOX0.wcFG_GjBSNVZCpP4NPC2xk6Dio8Jdd8vMb8e_rzXOFc"

# Supported languages (from API error message)
SUPPORTED_LANGUAGES = {
    "ach": "Acholi",
    "teo": "Ateso",
    "eng": "English",
    "lug": "Luganda",
    "lgg": "Lugbara",
    "nyn": "Runyankole"
}

def translate_text(text, source_lang, target_lang):
    """Send translation request to Sunbird AI API"""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "source_language": source_lang,
        "target_language": target_lang,
        "text": text
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise error for bad status codes
        return response.json()["output"]["translated_text"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def main():
    print("🌍 Sunbird AI Translator (Supported Languages)")
    for code, name in SUPPORTED_LANGUAGES.items():
        print(f"{code}: {name}")
    
    print("\nEnter 'quit' to exit")
    while True:
        text = input("\nText to translate: ")
        if text.lower() == 'quit':
            break
            
        source_lang = input("Source language code (e.g. 'eng'): ").strip()
        target_lang = input("Target language code (e.g. 'lug'): ").strip()
        
        if source_lang not in SUPPORTED_LANGUAGES or target_lang not in SUPPORTED_LANGUAGES:
            print("Error: Unsupported language code. Try again.")
            continue
            
        translated = translate_text(text, source_lang, target_lang)
        print(f"\nTranslation: {translated}")

if __name__ == "__main__":
    main()