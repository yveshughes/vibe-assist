# screen.py
import time
import io
import os
from datetime import datetime
from mss import mss
from PIL import Image
from . import analysis

def start(state, state_lock):
    """Thread for periodic screen analysis."""
    print("Screen analyzer starting...")

    # Create tmp directory for screenshots
    tmp_dir = "/tmp/vibe-assist-screenshots"
    os.makedirs(tmp_dir, exist_ok=True)
    print(f"Screenshots will be saved to: {tmp_dir}")

    with mss() as sct:
        while True:
            try:
                # Get a screenshot of the 1st monitor
                sct_img = sct.grab(sct.monitors[1])

                # Convert to PIL Image
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                # Convert to bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                image_bytes = img_byte_arr.getvalue()

                # Save screenshot to tmp folder with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(tmp_dir, f"screenshot_{timestamp}.png")
                with open(screenshot_path, 'wb') as f:
                    f.write(image_bytes)

                print(f"Screen captured ({len(image_bytes)} bytes) -> {screenshot_path}")

                # Analyze screenshot
                analysis.analyze_screen_proactively(image_bytes, state, state_lock)

            except Exception as e:
                print(f"Error capturing/analyzing screen: {e}")

            time.sleep(30)  # Analyze every 30 seconds (reduced from 10)

