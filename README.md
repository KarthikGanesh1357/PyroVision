# PyroVision: Wildfire Detection System using Satellite Imagery

## Project Overview

This project detects wildfires in near real-time using **satellite imagery** and generates **region-specific alerts**. The system combines **image preprocessing, CNN-based classification, and alert notifications**.

It also provides an interactive **Streamlit app** for uploading satellite images, predicting wildfire presence, and sending alerts based on geographic regions of interest (ROI).

---

## Key Features

- **Wildfire Detection:** CNN-based classification of satellite images as _Wildfire_ or _No Wildfire_.
- **Region-based Alerts:** Alerts are triggered only if the wildfire occurs within user-selected latitude/longitude bounds.
- **Interactive Streamlit App:** Upload images, view predictions, and trigger alerts.
- **Alert System:**
  - **Email notifications** via `smtplib` or AWS SES
  - **SMS / WhatsApp alerts** via Twilio API
  - **Push notifications** via Firebase Cloud Messaging
- **Data Preprocessing:** Handles corrupted images, rescales, and augments the dataset.
- **MLflow Integration:** Tracks model training, validation metrics, and loss.

---

## Technologies & Libraries

- Python 3.11+
- TensorFlow / Keras
- Pillow
- Streamlit
- MLflow
- Twilio API
- smtplib / AWS SES
- Firebase
- Sentinel Hub Python SDK
- OS, JSON, NumPy, Pandas

---

## Project Structure

```
pyrovision/
│
├── .gitignore
├── README.md
├── requirements.txt
├── app/
│   └── streamlit_app.py
├── src/
│   ├── alert_system.py
│   ├── alerts.py
│   ├── cnn_model.py
│   ├── config.py
│   ├── fetch_firms_gee.py
│   ├── preprocess.py
│   ├── test_sentinelhub.py
│   ├── visualize.py
│   └── data_collection/
│       └── sentinel2_downloader.py
├── data/
│   ├── raw/
│   └── processed/
└── wildfire_detection_model.h5
```

---

## Setup Instructions

1. **Clone Repository:**

   ```sh
   git clone https://github.com/<your-username>/wildfire-detection-app.git
   cd wildfire-detection-app
   ```

2. **Create Virtual Environment:**

   ```sh
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure Alerts:**

   - Update `src/alert_system.py` with your:
     - Email credentials or AWS SES keys
     - Twilio account SID, auth token, and sender number
     - Firebase project key for push notifications

5. **Run Streamlit App:**

   ```sh
   streamlit run app/streamlit_app.py
   ```

6. **Use the App:**
   - Upload satellite images
   - Select ROI (latitude/longitude bounds)
   - If wildfire is detected in ROI, alerts are sent via configured channels

---

## How It Works

### Data Collection

- Images fetched from Sentinel Hub (Sentinel-2) API.

### Preprocessing

- Verify images, remove corrupted files
- Resize to 150x150 pixels
- Augment dataset for CNN training

### Model Training

- CNN with 3 convolutional layers + max-pooling
- Binary classification (Wildfire / No Wildfire)
- Logs training loss and accuracy via MLflow

### Prediction

- Users upload images via Streamlit app
- Model predicts wildfire presence

### Alerts

- Checks if predicted fire is within user-defined ROI
- Sends email, SMS/WhatsApp, or push notification if true

---

## License

MIT License (add your license details here)
