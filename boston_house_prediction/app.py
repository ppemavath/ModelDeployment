import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Load the trained regression model
@st.cache_resource
def load_model():
    # Get the directory where app.py is located
    app_dir = Path(__file__).resolve().parent

    # Build the absolute path to the trained model
    model_path = app_dir / "boston_housing_model_v1_0.joblib"

    # Load the saved model
    return joblib.load(model_path)

model = load_model()


# Streamlit UI for Boston Housing Price Prediction
st.title("Boston Housing Price Prediction App")
st.write("This app predicts the median value of owner-occupied homes (`MEDV`) in $1000s based on Boston housing dataset features.")
st.write("Move the sliders below to adjust values and get a prediction.")

# Collect user input using sliders
CRIM = st.slider("Per capita crime rate by town (CRIM)", 0.0, 100.0, 0.2, 0.1)
ZN = st.slider("Proportion of residential land zoned for lots over 25,000 sq.ft. (ZN)", 0.0, 100.0, 12.0, 1.0)
INDUS = st.slider("Proportion of non-retail business acres per town (INDUS)", 0.0, 30.0, 11.0, 0.5)
NX = st.slider("Nitric oxides concentration (NX)", 0.0, 1.0, 0.55, 0.01)
RM = st.slider("Average number of rooms per dwelling (RM)", 3.0, 9.0, 6.3, 0.1)
AGE = st.slider("Proportion of owner-occupied units built prior to 1940 (AGE)", 0.0, 100.0, 65.0, 1.0)
DIS = st.slider("Weighted distances to employment centers (DIS)", 1.0, 12.0, 4.0, 0.1)
RAD = st.slider("Index of accessibility to radial highways (RAD)", 1, 24, 4, 1)
TAX = st.slider("Full-value property tax rate per $10,000 (TAX)", 100, 700, 300, 1)
PTRATIO = st.slider("Pupil-teacher ratio by town (PTRATIO)", 10.0, 25.0, 19.0, 0.1)
LSTAT = st.slider("% lower status of the population (LSTAT)", 0.0, 40.0, 12.0, 0.1)

# Categorical feature
CHAS = st.selectbox("Charles River dummy variable (CHAS)", ["0 (No)", "1 (Yes)"])
CHAS_value = 1 if CHAS.startswith("1") else 0

# Create input DataFrame
input_data = pd.DataFrame([{
    'CRIM': CRIM,
    'ZN': ZN,
    'INDUS': INDUS,
    'NX': NX,
    'RM': RM,
    'AGE': AGE,
    'DIS': DIS,
    'RAD': RAD,
    'TAX': TAX,
    'PTRATIO': PTRATIO,
    'LSTAT': LSTAT,
    'CHAS': CHAS_value
}])

# Predict button
if st.button("Predict MEDV"):
    predicted_price = model.predict(input_data)[0]
    st.success(f"💰 Estimated Median Value of Home (MEDV): ${predicted_price*1000:,.2f}")
