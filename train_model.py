import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import joblib

data = pd.read_csv("hepatitis.csv")
data.columns = data.columns.str.strip()
data.rename(columns={
    "Total_Bilirubin": "Bilirubin"   
}, inplace=True)
X = data[[
    "ALT",
    "AST",
    "Bilirubin",
    "Albumin",
    "Platelet_Count",
    "Hemoglobin"
]]
y = data["HBV_Status"]
X = X.fillna(0)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier()
}

best_model = None
best_score = 0

print("Training models...\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    score = accuracy_score(y_test, preds)

    print(f"{name}: {score:.4f}")

    if score > best_score:
        best_score = score
        best_model = model

print("\nBest model selected!")


joblib.dump(best_model, "hepatitis_model.pkl")