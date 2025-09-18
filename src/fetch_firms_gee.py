import ee
import geemap
import pandas as pd

# Authenticate and initialize
ee.Initialize(project='pyrovision-fires') 
# Define dataset
dataset = ee.FeatureCollection("FIRMS/VIIRS/NRT/VNP14IMGTDL_NRT")

# Define region (India bounding box)
region = ee.Geometry.Rectangle([68.0, 6.0, 97.5, 35.5])

# Filter for last 24h
fires = dataset.filterBounds(region).filterDate('2025-09-18', '2025-09-19')

# Export as Pandas DataFrame
fires_list = fires.toList(fires.size())
fires_info = fires_list.getInfo()

data = []
for f in fires_info:
    props = f['properties']
    coords = f['geometry']['coordinates']
    data.append({
        "latitude": coords[1],
        "longitude": coords[0],
        "brightness": props.get("brightness"),
        "confidence": props.get("confidence"),
        "frp": props.get("frp")
    })

df = pd.DataFrame(data)
print(df.head())

# Save to CSV
df.to_csv("data/firms_gee_latest.csv", index=False)
