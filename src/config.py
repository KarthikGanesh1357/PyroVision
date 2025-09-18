import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
API_KEY = os.getenv("FIRMS_API_KEY")

# You can change these defaults
PRODUCT = "VIIRS_SNPP_NRT"
REGION = "India"
TIME = "24h"  # options: 24h, 48h, 7d
