import streamlit as st
import pandas as pd
import requests

# Docker internal hostname for the Flask backend
BACKEND_URL = "http://backend:7860"

st.title("Airbnb Rental Price Prediction")
st.write("Predict rental prices using a trained machine-learning model.")

# ---------------------------------------
# Single-property prediction
# ---------------------------------------

st.subheader("Single Property Prediction")

room_type = st.selectbox(
    "Room Type",
    ["Entire home/apt", "Private room", "Shared room"]
)

accommodates = st.number_input(
    "Accommodates (Number of Guests)",
    min_value=1,
    value=2
)

bathrooms = st.number_input(
    "Bathrooms",
    min_value=1,
    step=1,
    value=2
)

cancellation_policy = st.selectbox(
    "Cancellation Policy",
    ["strict", "flexible", "moderate"]
)

cleaning_fee = st.selectbox(
    "Cleaning Fee Charged?",
    ["True", "False"]
)

instant_bookable = st.selectbox(
    "Instantly Bookable?",
    ["False", "True"]
)

review_scores_rating = st.number_input(
    "Review Score Rating",
    min_value=0.0,
    max_value=100.0,
    value=90.0,
    step=1.0
)

bedrooms = st.number_input(
    "Bedrooms",
    min_value=0,
    step=1,
    value=1
)

beds = st.number_input(
    "Beds",
    min_value=0,
    step=1,
    value=1
)

# Preserve the categorical values used in Notebook 8
property_data = {
    "room_type": room_type,
    "accommodates": accommodates,
    "bathrooms": bathrooms,
    "cancellation_policy": cancellation_policy,
    "cleaning_fee": cleaning_fee,
    "instant_bookable": "t" if instant_bookable == "True" else "f",
    "review_scores_rating": review_scores_rating,
    "bedrooms": bedrooms,
    "beds": beds
}

if st.button("Predict Rental Price", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/rental",
            json=property_data,
            timeout=30
        )

        response.raise_for_status()

        prediction = response.json()[
            "Predicted Price (in dollars)"
        ]

        st.success(
            f"Predicted Rental Price: ${prediction:,.2f}"
        )

    except (requests.RequestException, ValueError, KeyError) as error:
        st.error(f"Prediction failed: {error}")


# ---------------------------------------
# Batch rental-price prediction
# ---------------------------------------

st.divider()
st.subheader("Batch Rental Price Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV containing rental property details",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict Batch", type="primary"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/rentalbatch",
                files={"file": uploaded_file},
                timeout=120
            )

            response.raise_for_status()

            predictions = response.json()

            results_df = pd.DataFrame(
                [
                    {
                        "Property ID": property_id,
                        "Predicted Price ($)": price
                    }
                    for property_id, price in predictions.items()
                ]
            )

            st.success("Batch predictions completed!")
            st.dataframe(results_df, use_container_width=True)

        except (requests.RequestException, ValueError) as error:
            st.error(f"Batch prediction failed: {error}")
