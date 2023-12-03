import base64
from io import BytesIO

import pyautogui
from PIL import Image


def capture_and_encode_screenshot():
    # Capture a screenshot using pyautogui
    screenshot = pyautogui.screenshot()

    # Convert the PIL Image to a byte stream
    image_stream = BytesIO()
    screenshot.save(image_stream, format="PNG")
    screenshot.save("screenshot.png")

    # Encode the byte stream as base64
    base64_encoded_image = base64.b64encode(image_stream.getvalue()).decode("utf-8")

    return base64_encoded_image
