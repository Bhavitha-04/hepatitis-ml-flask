function highlightValue(id, value, min, max) {

    let element = document.getElementById(id);
    if (!element) return;

    element.innerText = value;

    let card = element.parentElement;

    if (value < min || value > max) {
        card.style.background = "#ffe5e5";
        card.style.border = "1px solid #ff4d4d";
        element.style.color = "#cc0000";
    } else {
        card.style.background = "#eaf7ea";
        card.style.border = "1px solid #4CAF50";
        element.style.color = "#2e7d32";
    }
}

async function uploadReport() {

    let fileInput = document.getElementById("report");

    if (fileInput.files.length === 0) {
        alert("Upload a report first");
        return;
    }

    let formData = new FormData();
    formData.append("report", fileInput.files[0]);

    try {

        let response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        let data = await response.json();

        console.log("API Response:", data);

        // 🔴 HANDLE BACKEND ERROR
        if (data.error) {
            alert("Error: " + data.error);

            document.getElementById("prediction").innerText =
                "Error occurred while processing report";

            return;
        }

        // ---------- HIGHLIGHT VALUES ----------
        highlightValue("altValue", data.ALT, 0, 40);
        highlightValue("astValue", data.AST, 0, 40);
        highlightValue("bilirubinValue", data.Bilirubin, 0, 1.2);
        highlightValue("albuminValue", data.Albumin, 3.5, 5);
        highlightValue("plateletsValue", data.Platelets, 150000, 450000);
        highlightValue("hemoglobinValue", data.Hemoglobin, 13, 17);

        // ---------- PREDICTION ----------
        document.getElementById("prediction").innerText =
            "Prediction: " + data.Prediction;

        // ---------- RISK ----------
        let risk = document.getElementById("risk");
        risk.innerText = "Risk Level: " + data.Risk;

        if (data.Risk === "Low") {
            risk.style.color = "green";
        } else if (data.Risk === "Moderate") {
            risk.style.color = "orange";
        } else {
            risk.style.color = "red";
        }

        // ---------- AI EXPLANATION ----------
        document.getElementById("aiExplanation").innerText =
            data.AI_Explanation;

        // ---------- REPORT TEXT ----------
        document.getElementById("reportText").innerText =
            data.report_text;

    } catch (error) {

        console.error("Fetch Error:", error);

        alert("Something went wrong. Please try again.");

        document.getElementById("prediction").innerText =
            "Server error. Try again.";

    }
}