import pytesseract
import torch
import requests
from PIL import Image
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import streamlit as st
import base64

# ✅ Configure Page
st.set_page_config(page_title="📜 Sanskrit Translator", layout="wide")

# 🎨 Custom CSS for Neon Theme
def set_page_bg():
    st.markdown(
        '''
        <style>
            body {
                background-color: #0f0f0f;
                color: #00ffcc;
                font-family: 'Arial', sans-serif;
            }
            .stApp {
                background-color: #121212;
                border-radius: 15px;
                padding: 20px;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #00ffcc !important;
                text-shadow: 0px 0px 10px #00ffcc;
            }
            .uploadedFile { color: #ffcc00 !important; }
            .stButton>button {
                background: linear-gradient(45deg, #ff00ff, #00ffff);
                border-radius: 10px;
                color: white;
                font-weight: bold;
            }
            .stTextInput>div>div>input {
                background-color: #1e1e1e;
                color: white;
            }
            .stSelectbox>div>div>select {
                background-color: #1e1e1e;
                color: white;
            }
        </style>
        ''',
        unsafe_allow_html=True
    )

set_page_bg()

# 🔑 API Configuration
GEMINI_API_KEY = "AIzaSyA83Z084MI-3oez2ANU_Lce5zU0QMupCCU"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# 🧠 Load Transformer Model (NLLB) for Translation
@st.cache_resource
def load_nllb_model():
    model_name = "facebook/nllb-200-1.3B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_nllb_model()

# 🖥 Configure Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# 📜 Function to Extract Text from Image
def extract_text(image):
    return pytesseract.image_to_string(image, lang="san").strip()

# 🔄 Function for Translation using Transformer Model (NLLB)
def translate_nllb(text, src_lang="san_Deva", tgt_lang="eng_Latn"):
    tokenizer.src_lang = src_lang
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_length=200,
        num_beams=5,
        temperature=0.7,
        repetition_penalty=2.5,
        length_penalty=1.5,
        no_repeat_ngram_size=3,
        early_stopping=True,
    )
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

def get_gemini_translation(text, target_lang="English"):
    """Translate text using Gemini API and return only the translation."""
    payload = {
        "contents": [
            {"parts": [{"text": f"Strictly translate this Sanskrit text to {target_lang} without explanation or additional context. Only output the translation:\n\n{text}"}]}
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        except KeyError:
            return "⚠️ Error parsing response."
    else:
        return f"❌ API Error: {response.status_code}"


# 🚀 Main UI
st.markdown("<h1 style='text-align: center;'>📜 Devnagri Image Translator</h1>", unsafe_allow_html=True)

# 📤 File Upload Section
uploaded_file = st.file_uploader("📤 Upload a Devnagri Image", type=["png", "jpg", "jpeg"], help="Upload an image containing Sanskrit text.")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Image", use_column_width=True)

    extracted_text = extract_text(image)
    st.subheader("📝 Extracted Text")
    st.code(extracted_text, language="plaintext")

    english_translation_nllb = translate_nllb(extracted_text)
    st.subheader("🔠 Translated English Text (Transformer Model)")
    st.code(english_translation_nllb, language="plaintext")

    english_translation_gemini = get_gemini_translation(extracted_text, "English")
    st.subheader("🔠 Translated English Text (Gemini)")
    st.code(english_translation_gemini, language="plaintext")

    lang_options = ["Telugu", "Tamil", "German", "French", "Spanish"]
    selected_lang = st.selectbox("🌍 Translate to Another Language", lang_options)

    if st.button("Translate", help="Translate the extracted text to the selected language."):
        translated_text = get_gemini_translation(english_translation_gemini, selected_lang)
        st.subheader(f"🌏 {selected_lang} Translation")
        st.code(translated_text, language="plaintext")
