import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("models/churn_model_v2.pkl")

st.title("Customer Churn Prediction")

# User Inputs

tenure = st.slider(
    "Customer Tenure (Months)",
    0,
    72,
    12
)

monthly_charges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    max_value=200.0,
    value=70.0
)

total_charges = st.number_input(
    "Total Charges",
    min_value=0.0,
    value=840.0
)

senior = st.selectbox(
    "Senior Citizen",
    [0, 1]
)

gender = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

contract = st.selectbox(
    "Contract Type",
    ["Month-to-month", "One year", "Two year"]
)

internet = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

tech_support = st.selectbox(
    "Tech Support",
    ["No", "Yes"]
)

online_security = st.selectbox(
    "Online Security",
    ["No", "Yes"]
)

paperless = st.selectbox(
    "Paperless Billing",
    ["No", "Yes"]
)

if st.button("Predict"):

    customer = {
        'SeniorCitizen': senior,
        'tenure': tenure,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges,

        'gender_Male': 1 if gender == "Male" else 0,
        'Partner_Yes': 0,
        'Dependents_Yes': 0,
        'PhoneService_Yes': 1,

        'MultipleLines_No phone service': 0,
        'MultipleLines_Yes': 1,

        'InternetService_Fiber optic': 1 if internet == "Fiber optic" else 0,
        'InternetService_No': 1 if internet == "No" else 0,
       
        'OnlineSecurity_No internet service': 0,
        'OnlineSecurity_Yes': 1 if online_security == "Yes" else 0,

        'OnlineBackup_No internet service': 0,
        'OnlineBackup_Yes': 0,

        'DeviceProtection_No internet service': 0,
        'DeviceProtection_Yes': 0,

        'TechSupport_No internet service': 0,
        'TechSupport_Yes': 1 if tech_support == "Yes" else 0,

        'StreamingTV_No internet service': 0,
        'StreamingTV_Yes': 1,

        'StreamingMovies_No internet service': 0,
        'StreamingMovies_Yes': 1,

        'Contract_One year': 1 if contract == "One year" else 0,
        'Contract_Two year': 1 if contract == "Two year" else 0,

        'PaperlessBilling_Yes': 1 if paperless == "Yes" else 0,

        'PaymentMethod_Credit card (automatic)': 0,
        'PaymentMethod_Electronic check': 1,
        'PaymentMethod_Mailed check': 0
    }

    input_df = pd.DataFrame([customer])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error(
            f"Likely to Churn ({probability:.2%})"
        )
    else:
        st.success(
            f"Likely to Stay ({1-probability:.2%})"
        )

    st.metric(
        "Churn Probability",
        f"{probability:.2%}"
    )
    
    if probability > 0.7:
     st.warning(
        "High churn risk. Consider retention offers, discounts, or proactive customer support."
      )

    elif probability > 0.4:
     st.info(
        "Medium churn risk. Monitor customer engagement and satisfaction."
     )

    else:
     st.success(
        "Low churn risk. Customer is likely to remain with the company."
     )