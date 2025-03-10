# Deep-Learning-Text-Recognition-And-Translation-From-Devanagari-Scripts
Our project utilizes Optical Character Recognition (OCR) to extract Devanagari text from images and translates it into English using Transformer-based AI models. Additionally, it supports multi-language translation, enabling conversions beyond English, such as Sanskrit → Telugu and Sanskrit → German . The model is deployed as a user-friendly web app, making it accessible for seamless interaction and real-time translations.
# Features
* Extract text from Devanagari images using Tesseract OCR.
* Translate Sanskrit text to English using NLLB (Neural Machine Translation).
* Further translate English text into other languages.
* User-friendly interface with Streamlit.
# Technologies Used
* Python
* Streamlit (for UI)
* Tesseract OCR (for text extraction)
* Hugging Face Transformers (NLLB-200)
* Google Gemini API (for translations)
* PIL (Pillow) (for image handling)
* Requests (for API communication)
# How It Works
* Upload an Image – Upload an image containing Sanskrit text in Devanagari script.
* Text Extraction – The app extracts text using Tesseract OCR.
* Translation to English – The extracted text is translated into English using NLLB-200 and Gemini API.
* Multi-Language Translation – Users can translate the English text into Telugu, Tamil, German, French, or Spanish.
# Usage
## Run the Streamlit App
```
streamlit run app.py
```
