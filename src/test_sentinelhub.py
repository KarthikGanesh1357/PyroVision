from sentinelhub import SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType

config = SHConfig()

# Should print your client ID
print("Client ID:", config.sh_client_id)

# Define a small bounding box (somewhere in California wildfire area for test)
bbox = BBox(bbox=[-122.5, 37.5, -122.3, 37.7], crs=CRS.WGS84)

# Simple request: True Color image
request = SentinelHubRequest(
    evalscript="""
    //VERSION=3
    function setup() {
      return {
        input: ["B04", "B03", "B02"],
        output: { bands: 3 }
      };
    }

    function evaluatePixel(sample) {
      return [sample.B04, sample.B03, sample.B02];
    }
    """,
    input_data=[SentinelHubRequest.input_data(DataCollection.SENTINEL2_L2A)],
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    bbox=bbox,
    size=(256, 256),
    config=config,
)

image = request.get_data()
print("Downloaded image shape:", image[0].shape)
