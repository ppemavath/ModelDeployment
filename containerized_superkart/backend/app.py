import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask("SuperKart Sales Prediction API")
MODEL_PATH = Path(__file__).resolve().parent / "superkart_model.joblib"
model = joblib.load(MODEL_PATH)
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area",
    "Product_MRP", "Store_Size", "Store_Location_City_Type",
    "Store_Type", "Product_Id_char", "Store_Age_Years", "Product_Type_Category"
]

def prepare(frame):
    missing = [col for col in FEATURES if col not in frame.columns]
    if missing:
        raise ValueError(f"Missing model features: {missing}")
    frame = frame.loc[:, FEATURES].copy()
    frame["Product_Sugar_Content"] = frame["Product_Sugar_Content"].replace({"reg": "Regular"})
    return frame

@app.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

@app.post("/v1/predict")
def predict_single():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Expected a JSON object"}), 400
    try:
        X = prepare(pd.DataFrame([payload]))
        value = float(model.predict(X)[0])
        if not np.isfinite(value):
            raise ValueError("Model returned a non-finite prediction")
    except (ValueError, TypeError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"Predicted_Sales": round(value, 2)})

@app.post("/v1/predictbatch")
def predict_batch():
    if "file" not in request.files:
        return jsonify({"error": "Upload a CSV in form field 'file'"}), 400
    try:
        incoming = pd.read_csv(request.files["file"])
        X = prepare(incoming)
        predictions = model.predict(X)
        if not np.isfinite(predictions).all():
            raise ValueError("Model returned non-finite batch predictions")
        results = {str(i): round(float(value), 2) for i, value in enumerate(predictions)}
    except (ValueError, TypeError, KeyError, pd.errors.EmptyDataError) as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7860, debug=False)
