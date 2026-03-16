import streamlit as st
import pandas as pd
import joblib

model = joblib.load('groundwater_rf_model.pkl')

st.title('Groundwater Potability Predictor')
st.write('Enter water quality parameters to predict if the water is safe to drink.')

ph = st.slider('pH', 0.0, 14.0, 7.0)
hardness = st.number_input('Hardness (mg/L)', value=500.0)
solids = st.number_input('Solids/TDS (ppm)', value=15000.0)
chloramines = st.number_input('Chloramines (ppm)', value=6.5)
sulfate = st.number_input('Sulfate (mg/L)', value=400.0)
conductivity = st.number_input('Conductivity (μS/cm)', value=400.0)
organic_carbon = st.number_input('Organic Carbon (ppm)', value=12.0)
trihalomethanes = st.number_input('Trihalomethanes (μg/L)', value=400.0)
turbidity = st.number_input('Turbidity (NTU)', value=6)

if st.button('Predict'):
    input_data = pd.DataFrame([{
        'ph': ph,
        'Hardness': hardness,
        'Solids': solids,
        'Chloramines': chloramines,
        'Sulfate': sulfate,
        'Conductivity': conductivity,
        'Organic_carbon': organic_carbon,
        'Trihalomethanes': trihalomethanes,
        'Turbidity': turbidity
    }])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    confidence = probability[0].max()

    if prediction[0] == 1:
        st.success(f'✅ Potable — Safe to drink ({confidence:.1%} confidence)')
    else:
        st.error(f'❌ Not potable — Unsafe to drink ({confidence:.1%} confidence)')
        
    if confidence < 0.65:
        st.warning('⚠️ Low confidence — recommend lab verification')