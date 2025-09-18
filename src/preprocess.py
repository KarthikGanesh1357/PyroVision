import os
import glob
import numpy as np
import rasterio
from rasterio import Affine
from rasterio.enums import Resampling
import matplotlib.pyplot as plt

RAW_FOLDER = "C:/pyrovision/data/raw"
PROCESSED_FOLDER = "C:/pyrovision/data/processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# ------------------------
# Helper functions
# ------------------------
def scale_to_uint8(band, scale_factor=10000):
    """Scale Sentinel-2 float bands to 0-255 uint8."""
    band = np.clip(band / scale_factor, 0, 1)
    return (band * 255).astype(np.uint8)

def compute_nbr(nir, swir2):
    """Normalized Burn Ratio: (NIR - SWIR2)/(NIR + SWIR2)"""
    return np.where((nir+swir2)==0, 0, (nir - swir2)/(nir + swir2))

def compute_ndvi(nir, red):
    """Normalized Difference Vegetation Index: (NIR - RED)/(NIR + RED)"""
    return np.where((nir+red)==0, 0, (nir - red)/(nir + red))

# ------------------------
# Main preprocessing loop
# ------------------------
tiff_files = glob.glob(os.path.join(RAW_FOLDER, "*.tif"))
print(f"Found {len(tiff_files)} raw TIFFs.")

for tfile in tiff_files:
    with rasterio.open(tfile) as src:
        img = src.read()  # shape: (bands, H, W)
        meta = src.meta.copy()
    
    # Bands order in our downloader: [B04, B03, B02, B08, B12]
    red, green, blue, nir, swir2 = img

    # Scaled RGB for visualization / optional input
    rgb_scaled = np.stack([
        scale_to_uint8(red),
        scale_to_uint8(green),
        scale_to_uint8(blue)
    ], axis=-1)

    # Compute indices
    nbr = compute_nbr(nir, swir2)
    ndvi = compute_ndvi(nir, red)

    # Save RGB and NBR separately
    base_name = os.path.splitext(os.path.basename(tfile))[0]

    # Save RGB
    rgb_meta = meta.copy()
    rgb_meta.update({
        "count": 3,
        "dtype": "uint8"
    })
    with rasterio.open(os.path.join(PROCESSED_FOLDER, f"{base_name}_RGB.tif"), "w", **rgb_meta) as dst:
        dst.write(np.transpose(rgb_scaled, (2,0,1)))

    # Save NBR
    nbr_meta = meta.copy()
    nbr_meta.update({
        "count": 1,
        "dtype": "float32"
    })
    with rasterio.open(os.path.join(PROCESSED_FOLDER, f"{base_name}_NBR.tif"), "w", **nbr_meta) as dst:
        dst.write(nbr.astype(np.float32), 1)

print("Preprocessing complete. Scaled RGB and NBR saved in:", PROCESSED_FOLDER)
