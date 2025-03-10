import requests
import json

GEMINI_API_KEY = "AIzaSyDzoVCksAnNQiPMy2glcPmFR0mLILqAgyE"  # Replace with your API Key

def enhance_english_translation(text):
    """Enhance Sanskrit-to-English translation using Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"Extracted text: {text}\n\nImprove this translation to fluent and meaningful English."

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Error: Unexpected response format."
    else:
        return f"Translation failed. API Response: {response.text}"

def translate_to_languages(text, target_lang):
    """Translate English text to another language using Gemini API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"Translate this English text to {target_lang}:\n\n{text}"

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Error: Unexpected response format."
    else:
        return f"Translation failed. API Response: {response.text}"
