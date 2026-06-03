import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\bhavitha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_value(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except:
            return 0
    return 0

img = Image.open("report.png")

text = pytesseract.image_to_string(img)

print("OCR TEXT:\n", text)

alt = extract_value(r"ALT\s*[:\-]?\s*([0-9.]+)", text)
ast = extract_value(r"AST\s*[:\-]?\s*([0-9.]+)", text)
bilirubin = extract_value(r"Bilirubin\s*[:\-]?\s*([0-9.]+)", text)

print("ALT:", alt)
print("AST:", ast)
print("Bilirubin:", bilirubin)