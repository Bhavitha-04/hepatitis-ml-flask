import pytesseract
from PIL import Image
import joblib
import re

# path of OCR engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\bhavitha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# load ML model
model = joblib.load("hepatitis_model.pkl")

# function to safely extract values
def extract_value(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except:
            return 0
    return 0

# open blood report image
img = Image.open("report.png")

# OCR read text
text = pytesseract.image_to_string(img)

print("OCR TEXT:\n", text)

# extract medical values
alt = extract_value(r"ALT\s*[:\-]?\s*([0-9.]+)", text)
ast = extract_value(r"AST\s*[:\-]?\s*([0-9.]+)", text)
bilirubin = extract_value(r"Bilirubin\s*[:\-]?\s*([0-9.]+)", text)

print("ALT:", alt)
print("AST:", ast)
print("Bilirubin:", bilirubin)

# features for ML model
features = [[0]*19]

features[0][0] = alt
features[0][1] = ast
features[0][2] = bilirubin

# prediction
prediction = model.predict(features)

print("Prediction:", prediction[0])