import sdk.api as api
from PIL import Image
from threading import Lock
from config import DIR_PATH
import requests
import io

roll = 0
roll_lock = Lock()

TEMP_SIZE = 10
# store 10 temp images locally.

def save_image(img: Image) -> str:
    global roll
    with roll_lock:
        cur = roll
        roll = (roll + 1) % TEMP_SIZE
    filename = f"{DIR_PATH}/temp/image_{cur}.png"
    img.save(filename)
    return filename

def download_image(url: str) -> Image:
    resp = requests.get(url)
    return Image.open(io.BytesIO(resp.content))

