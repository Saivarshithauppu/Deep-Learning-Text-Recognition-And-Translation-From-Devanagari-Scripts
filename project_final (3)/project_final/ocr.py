import pytesseract
from PIL import Image

# Set Tesseract OCR Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR."""
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img, lang='san')  # 'san' for Sanskrit
    return extracted_text.strip()
