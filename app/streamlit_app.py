import streamlit as st
import os
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from alert_system import send_email_alert, send_sms_alert, send_push_alert, is_in_region  # import your alert functions

# Load trained model
model = load_model("wildfire_detection_model.h5")

IMG_HEIGHT, IMG_WIDTH = 150, 150

st.title("🔥 Wildfire Detection System")

# --- Region Selection ---
st.sidebar.header("Region of Interest")
min_lat = st.sidebar.number_input("Min Latitude", value=18.5)
max_lat = st.sidebar.number_input("Max Latitude", value=20.0)
min_lon = st.sidebar.number_input("Min Longitude", value=72.0)
max_lon = st.sidebar.number_input("Max Longitude", value=73.5)

ROI = {"min_lat": min_lat, "max_lat": max_lat, "min_lon": min_lon, "max_lon": max_lon}

# --- Image Upload ---
st.header("Upload Satellite Image")
uploaded_file = st.file_uploader("Choose a satellite image (TIFF/PNG/JPG)", type=["tif", "png", "jpg"])

fires_in_roi = []

if uploaded_file:
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
    # Predict wildfire
    img = image.load_img(uploaded_file, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)[0][0]
    label = "Wildfire" if prediction > 0.5 else "No Wildfire"
    
    st.subheader(f"Prediction: {label}")
    
    # If wildfire, ask for coordinates
    if label == "Wildfire":
        st.subheader("Specify Fire Location for Alert")
        lat = st.number_input("Latitude", value=min_lat)
        lon = st.number_input("Longitude", value=min_lon)
        
        if is_in_region(lat, lon, ROI):
            fires_in_roi.append(f"Uploaded Image ({lat}, {lon})")
            st.success("Fire detected in ROI! Alert will be sent.")
            
            if st.button("Send Alerts"):
                send_email_alert(fires_in_roi)
                send_sms_alert(fires_in_roi)
                send_push_alert(fires_in_roi)
                st.balloons()
                st.info("Alerts sent successfully!")
        else:
            st.warning("Fire detected, but outside the selected ROI. No alerts sent.")
