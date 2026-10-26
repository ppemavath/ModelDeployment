import pandas as pd
import requests
import streamlit as st

BACKEND_URL = "http://backend:7860"
st.set_page_config(page_title="SuperKart Sales Forecasting", page_icon="🛒", layout="wide")
st.title("SuperKart | Product–Store Sales Prediction")
st.caption("Historical product/store revenue prediction. Not a validated future-quarter time-series forecast.")
st.subheader("Single Product–Store Prediction")

with st.form("single_predict"):
    left, right = st.columns(2)
    with left:
        product_weight = st.number_input("Product Weight", value=12.66, min_value=0.0)
        sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        allocated = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
        mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"], index=1)
    with right:
        city = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"], index=1)
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart", "Supermarket Type3"], index=1)
        prefix = st.selectbox("Product ID Prefix", ["FD", "DR", "NC"])
        store_age = st.number_input("Store Age (2025 reference years)", min_value=0, max_value=150, value=16)
        category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"], index=1)
    submit = st.form_submit_button("Predict Sales")

if submit:
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": sugar,
        "Product_Allocated_Area": allocated,
        "Product_MRP": mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city,
        "Store_Type": store_type,
        "Product_Id_char": prefix,
        "Store_Age_Years": store_age,
        "Product_Type_Category": category
    }
    try:
        r = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=30)
        r.raise_for_status()
        st.success(f"Predicted product–store sales: {r.json()['Predicted_Sales']:,.2f}")
    except (requests.RequestException, KeyError, ValueError) as err:
        st.error(f"Prediction request failed: {err}")

st.divider()
st.subheader("Batch Prediction")
uploaded = st.file_uploader("Upload a CSV containing the ten model features", type=["csv"])
if uploaded is not None:
    try:
        source = pd.read_csv(uploaded)
        st.dataframe(source.head(10))
        if st.button("Predict Batch"):
            uploaded.seek(0)
            r = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded}, timeout=120)
            r.raise_for_status()
            prediction = r.json()
            results = pd.DataFrame({"Row": list(prediction.keys()), "Predicted Sales": list(prediction.values())})
            st.success("Batch prediction completed")
            st.dataframe(results)
            st.download_button("Download predicted sales CSV", results.to_csv(index=False),
                               file_name="superkart_predictions.csv", mime="text/csv")
    except (requests.RequestException, ValueError, pd.errors.ParserError) as err:
        st.error(f"Batch prediction failed: {err}")
