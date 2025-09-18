import os
import numpy as np
from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType, bbox_to_dimensions

# ------------------------
# Configuration
# ------------------------
config = SHConfig()
OUTPUT_FOLDER = "C:/pyrovision/data/raw"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# AOI: India bounding box [min_lon, min_lat, max_lon, max_lat]
AOI = [68.0, 6.0, 97.5, 35.5]
RESOLUTION = 60  # meters per pixel
MAX_PIXELS = 2500  # Sentinel Hub limit per dimension

# Date range
START_DATE = "2025-09-01"
END_DATE = "2025-09-05"

# ------------------------
# Helper: generate tiles
# ------------------------
def generate_tiles(aoi, resolution=RESOLUTION, max_pixels=MAX_PIXELS):
    min_lon, min_lat, max_lon, max_lat = aoi
    width = int((max_lon - min_lon) / (resolution / 111000))
    height = int((max_lat - min_lat) / (resolution / 111000))
    
    lon_splits = np.linspace(min_lon, max_lon, int(np.ceil(width / max_pixels)) + 1)
    lat_splits = np.linspace(min_lat, max_lat, int(np.ceil(height / max_pixels)) + 1)
    
    tiles = []
    for i in range(len(lon_splits)-1):
        for j in range(len(lat_splits)-1):
            tiles.append([lon_splits[i], lat_splits[j], lon_splits[i+1], lat_splits[j+1]])
    return tiles

# ------------------------
# Evalscript: True Color + NBR bands
# ------------------------
EVALSCRIPT = """
//VERSION=3
function setup() {
    return { input: ["B04","B03","B02","B08","B12"], output: {bands:5} };
}
function evaluatePixel(sample) {
    return [sample.B04,sample.B03,sample.B02,sample.B08,sample.B12];
}
"""

# ------------------------
# Download loop
# ------------------------
tiles = generate_tiles(AOI)
print(f"Generated {len(tiles)} tiles.")

for idx, t in enumerate(tiles):
    tile_bbox = BBox(bbox=t, crs=CRS.WGS84)
    size = bbox_to_dimensions(tile_bbox, resolution=RESOLUTION)
    
    request = SentinelHubRequest(
        evalscript=EVALSCRIPT,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A,
            time_interval=(START_DATE, END_DATE)
        )],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=tile_bbox,
        size=size,
        data_folder=OUTPUT_FOLDER,
        config=config
    )
    
    print(f"Downloading tile {idx+1}/{len(tiles)}: {t}")
    try:
        request.get_data(save_data=True)
    except Exception as e:
        print(f"Failed to download tile {idx+1}: {e}")

print("All tiles processed.")
