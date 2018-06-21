import requests
import base64
from PIL import Image
from io import BytesIO


# Generate image thumbnail by downloading image URL, creating a Pillow
# image from it, then using the Image.thumbnail method to resize it,
# finally Base64-encoding the resulting PNG image and making a data
# URL from it.
def make_thumbnail(url, sz):
    # Download original image URL.
    r = requests.get(url)

    # Create PIL image from in-memory stream.
    img = Image.open(BytesIO(r.content))

    # Generate our thumbnail image.
    img.thumbnail((sz, sz))

    # Using another in-memory stream...
    with BytesIO() as fp:
        # Extract the image as a PNG.
        img.save(fp, format='PNG')

        # Base-64 encode the image data (and convert to a Python
        # string with "decode").
        b64 = base64.b64encode(fp.getbuffer()).decode()

        # Make the final data URI, showing that it's Base-64 encoded
        # PNG data.
        data = 'data:image/png;base64,' + b64
    return data
