from flask import Flask, render_template, request, jsonify, redirect, url_for
import pytesseract
from PIL import Image
import joblib
import re
from pdf2image import convert_from_bytes
import shap
import numpy as np

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\bhavitha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

model = joblib.load("hepatitis_model.pkl")
def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace(":", " ")
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)
    return text

def format_report_text(text):
    keywords = ["ALT", "AST", "Bilirubin", "Albumin", "Platelets", "Hemoglobin"]
    for word in keywords:
        text = text.replace(word, "\n" + word)
    return text.strip()

def extract_medical_value(keyword, text):
    pattern = rf"{keyword}[^0-9]*([0-9]+\.?[0-9]*)"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return float(matches[0]) if matches else 0


@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")
    if name:
        return render_template("ui.html", username=name)
    return redirect(url_for("login_page"))

@app.route("/ui")
def ui_dashboard():
    return render_template("ui.html")

@app.route("/index1")
def home():
    return render_template("index1.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/ai")
def ai():
    return render_template("ai.html")

@app.route("/management")
def management():
    return render_template("management.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files["report"]
        if file.filename.endswith(".pdf"):
            images = convert_from_bytes(file.read())
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img, config="--psm 6")
        else:
            img = Image.open(file)
            text = pytesseract.image_to_string(img, config="--psm 6")

        text = clean_text(text)
        formatted_text = format_report_text(text)

        alt = extract_medical_value("ALT", text)
        ast = extract_medical_value("AST", text)
        bilirubin = extract_medical_value("Bilirubin", text)
        albumin = extract_medical_value("Albumin", text)
        platelets = extract_medical_value("Platelets", text)
        hemoglobin = extract_medical_value("Hemoglobin", text)

        if bilirubin == 0:
            bilirubin = 1.0
        if albumin == 0:
            albumin = 4.0
        if platelets == 0:
            platelets = 200000
        if hemoglobin == 0:
            hemoglobin = 13.0

        features = np.array([[
            alt,
            ast,
            bilirubin,
            albumin,
            platelets,
            hemoglobin
        ]])


        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        prediction_label = "Hepatitis Detected" if prediction == 1 else "No Hepatitis"
        if prob < 0.3:
            risk = "Low"
        elif prob < 0.7:
            risk = "Moderate"
        else:
            risk = "High"

        if alt > 200 or ast > 200 or bilirubin > 3:
            prediction_label = "Hepatitis Detected"
            risk = "High"
        shap_result = {}
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(features)[1]

            shap_result = {
                "ALT": float(shap_values[0][0]),
                "AST": float(shap_values[0][1]),
                "Bilirubin": float(shap_values[0][2]),
                "Albumin": float(shap_values[0][3]),
                "Platelets": float(shap_values[0][4]),
                "Hemoglobin": float(shap_values[0][5])
            }
        except:
            shap_result = {}

        explanation = []

        if alt > 40:
            explanation.append("ALT is very high indicating liver damage")

        if ast > 40:
            explanation.append("AST is very high indicating liver stress")

        if bilirubin > 1.2:
            explanation.append("Bilirubin is elevated indicating liver dysfunction")

        if albumin < 3.5:
            explanation.append("Low albumin suggests poor liver function")

        if platelets < 150000:
            explanation.append("Low platelets may indicate liver disease")

        if hemoglobin < 12:
            explanation.append("Low hemoglobin suggests anemia")

 
        if shap_result:
            for feature, value in shap_result.items():
                if value > 0:
                    explanation.append(f"{feature} increases risk")
                else:
                    explanation.append(f"{feature} reduces risk")

        ai_explanation = ". ".join(explanation)

    
        return jsonify({
            "ALT": alt,
            "AST": ast,
            "Bilirubin": bilirubin,
            "Albumin": albumin,
            "Platelets": platelets,
            "Hemoglobin": hemoglobin,
            "Prediction": prediction_label,
            "Probability": float(prob),
            "Risk": risk,
            "SHAP_Values": shap_result,
            "AI_Explanation": ai_explanation,
            "report_text": formatted_text
        })

    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(debug=True)