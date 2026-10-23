import numpy as np
import pandas as pd
import joblib

from pathlib import Path
from flask import Flask, request, jsonify

# Initialize Flask
rental_price_predictor_api = Flask(
    "Airbnb Rental Price Predictor"
)

# Load model from the same directory as app.py
app_dir = Path(__file__).resolve().parent
model_path = app_dir / "rental_price_prediction_model_v1_0.joblib"

model = joblib.load(model_path)

# Features used by the trained model
FEATURES = [
    "room_type",
    "accommodates",
    "bathrooms",
    "cancellation_policy",
    "cleaning_fee",
    "instant_bookable",
    "review_scores_rating",
    "bedrooms",
    "beds"
]


@rental_price_predictor_api.get("/")
def home():
    return "Welcome to the Airbnb Rental Price Prediction API!"


# Single-property prediction
@rental_price_predictor_api.post("/v1/rental")
def predict_rental_price():

    property_data = request.get_json(silent=True)

    if not isinstance(property_data, dict):
        return jsonify({"error": "Expected a JSON object"}), 400

    missing = [f for f in FEATURES if f not in property_data]

    if missing:
        return jsonify({"error": f"Missing features: {missing}"}), 400

    input_data = pd.DataFrame([property_data])[FEATURES]

    # Predict logarithmic rental price
    predicted_log_price = model.predict(input_data)[0]

    # Convert back to dollars
    predicted_price = round(
        float(np.exp(predicted_log_price)), 2
    )

    return jsonify({
        "Predicted Price (in dollars)": predicted_price
    })


# Batch rental-price prediction
@rental_price_predictor_api.post("/v1/rentalbatch")
def predict_rental_price_batch():

    if "file" not in request.files:
        return jsonify({"error": "CSV file is required"}), 400

    uploaded_file = request.files["file"]

    input_data = pd.read_csv(uploaded_file)

    missing = [f for f in FEATURES if f not in input_data.columns]

    if missing:
        return jsonify({"error": f"Missing features: {missing}"}), 400

    # Preserve property IDs, but do not pass them to the model
    if "id" in input_data.columns:
        property_ids = input_data["id"].tolist()
    else:
        property_ids = list(range(1, len(input_data) + 1))

    model_input = input_data[FEATURES]

    predicted_log_prices = model.predict(model_input)

    predicted_prices = [
        round(float(np.exp(price)), 2)
        for price in predicted_log_prices
    ]

    results = {
        str(property_id): price
        for property_id, price in zip(property_ids, predicted_prices)
    }

    return jsonify(results)


if __name__ == "__main__":
    rental_price_predictor_api.run(
        host="127.0.0.1",
        port=7860,
        debug=False
    )
