import json
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
import firebase_admin
from firebase_admin import messaging, credentials

# --- Region of Interest ---
ROI = {"min_lat": 18.5, "max_lat": 20.0, "min_lon": 72.0, "max_lon": 73.5}

# --- Alert credentials ---
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH = "your_twilio_auth_token"
TWILIO_FROM = "+1234567890"
TWILIO_TO = "+919XXXXXXXXX"

FIREBASE_JSON = r"path/to/firebase_service_account.json"

# --- Initialize Firebase ---
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_JSON)
    firebase_admin.initialize_app(cred)

# --- Helper: Check if coordinates in ROI ---
def is_in_region(lat, lon, roi):
    return roi["min_lat"] <= lat <= roi["max_lat"] and roi["min_lon"] <= lon <= roi["max_lon"]

# --- Alerts ---
def send_email_alert(fire_list):
    body = "Wildfires detected in the following locations:\n" + "\n".join(fire_list)
    msg = MIMEText(body)
    msg['Subject'] = "🔥 Wildfire Alert"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

def send_sms_alert(fire_list):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    message_body = "🔥 Wildfires detected:\n" + "\n".join(fire_list)
    message = client.messages.create(body=message_body, from_=TWILIO_FROM, to=TWILIO_TO)
    print("SMS sent:", message.sid)

def send_push_alert(fire_list):
    message = messaging.Message(
        notification=messaging.Notification(
            title="🔥 Wildfire Alert",
            body="Wildfires detected: " + ", ".join(fire_list)
        ),
        topic="wildfire_alerts"
    )
    response = messaging.send(message)
    print("Push notification sent:", response)

# --- Load new images metadata with predictions ---
NEW_IMAGES_META = r"C:\pyrovision\data\new_images_metadata.json"
with open(NEW_IMAGES_META, "r") as f:
    images_metadata = json.load(f)

# --- Detect fires in ROI ---
fires_in_roi = []
for meta in images_metadata:
    # meta should have: image_path, latitude, longitude, prediction ("Wildfire"/"No Wildfire")
    if meta["prediction"] == "Wildfire":
        if is_in_region(meta["latitude"], meta["longitude"], ROI):
            fires_in_roi.append(f"{meta['image_path']} ({meta['latitude']},{meta['longitude']})")

# --- Send alerts if any ---
if fires_in_roi:
    send_email_alert(fires_in_roi)
    send_sms_alert(fires_in_roi)
    send_push_alert(fires_in_roi)
else:
    print("No new wildfires detected in the selected region.")
