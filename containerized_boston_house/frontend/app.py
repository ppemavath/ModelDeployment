import streamlit as st
import pandas as pd
import requests

# Docker internal hostname of the Flask backend
BACKEND_URL = "http://backend:7860"

# Must match the name expected by your saved model/backend.
# Change to "NOX" if that is what you confirmed in Step 2.
OXIDE_FIELD = "NX"

st.title("Boston Housing Price Prediction App")

st.write(
    "Predict median house values using the historical "
    "Boston Housing dataset. Predictions are expressed "
    "in thousands of dollars."
)

st.subheader("Single House Prediction")

CRIM = st.slider("Per capita crime rate (CRIM)", 0.0, 100.0, 0.2, 0.1)
ZN = st.slider("Residential land zoning (ZN)", 0.0, 100.0, 12.0, 1.0)
INDUS = st.slider("Non-retail business acres (INDUS)", 0.0, 30.0, 11.0, 0.5)

CHAS = st.selectbox(
    "Charles River boundary (CHAS)",
    ["0 (No)", "1 (Yes)"]
)
CHAS_value = 1 if CHAS.startswith("1") else 0

NX = st.slider("Nitric oxides concentration", 0.0, 1.0, 0.55, 0.01)
RM = st.slider("Average rooms per dwelling (RM)", 3.0, 9.0, 6.3, 0.1)
AGE = st.slider("Older owner-occupied units (AGE)", 0.0, 100.0, 65.0, 1.0)
DIS = st.slider("Distance to employment centers (DIS)", 1.0, 12.0, 4.0, 0.1)
RAD = st.slider("Highway accessibility (RAD)", 1, 24, 4, 1)
TAX = st.slider("Property tax rate (TAX)", 100, 700, 300, 1)
PTRATIO = st.slider("Pupil-teacher ratio (PTRATIO)", 10.0, 25.0, 19.0, 0.1)
LSTAT = st.slider("Lower-status population percentage (LSTAT)", 0.0, 40.0, 12.0, 0.1)

# Use the same feature names as the Flask API
input_data = {
    "CRIM": CRIM,
    "ZN": ZN,
    "INDUS": INDUS,
    "CHAS": CHAS_value,
    OXIDE_FIELD: NX,
    "RM": RM,
    "AGE": AGE,
    "DIS": DIS,
    "RAD": RAD,
    "TAX": TAX,
    "PTRATIO": PTRATIO,
    "LSTAT": LSTAT
}

if st.button("Predict", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/house",
            json=input_data,
            timeout=30
        )
        response.raise_for_status()

        predicted_price = response.json()["Predicted_MEDV"]

        st.success(
            f"Predicted Median House Value: "
            f"${predicted_price * 1000:,.2f}"
        )

    except (requests.RequestException, ValueError, KeyError) as error:
        st.error(f"Prediction request failed: {error}")


# Batch prediction
st.subheader("Batch House Price Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file containing house features",
    type=["csv"]
)

if uploaded_file is not None:
    if st.button("Predict for Batch", type="primary"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/housebatch",
                files={"file": uploaded_file},
                timeout=60
            )
            response.raise_for_status()

            results = response.json()

            st.success("Batch predictions completed successfully!")
            st.dataframe(pd.DataFrame(results))

        except (requests.RequestException, ValueError) as error:
            st.error(f"Batch prediction failed: {error}")
