import requests
import numpy as np
import cv2
import base64
from PIL import Image
import time
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
bearer_token = os.getenv('FASHN_BEARER_TOKEN')

def load_image(file_name):
    img = Image.open(file_name)
    img = img.convert("RGB")  # Ensure the image is in RGB format
    img.load()
    data = np.asarray(img, dtype="uint8")  # Change dtype to uint8
    return data

def encode_img_to_base64(img: np.array) -> str:
    """Encodes an image as a JPEG in Base64 format."""
    # Convert the image from RGB to BGR
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Encode the image to JPEG format
    _, img_encoded = cv2.imencode(".jpg", img_bgr)
    img_bytes = img_encoded.tobytes()

    # Encode to Base64
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    img = f"data:image/jpeg;base64,{img_base64}"
    return img

def fetch_and_save_image(url, filename):
    img_data = requests.get(url).content

    with open(filename, 'wb') as handler:
        handler.write(img_data)

def get_virtual_try_on(
    model_image: str,
    garment_image: str,
    category: str,
    nsfw_filter: bool = True,
    cover_feet: bool = False,
    adjust_hands: bool = False,
    restore_background: bool = False,
    restore_clothes: bool = False,
    garment_photo_type: str = "auto",
    long_top: bool = False,
    mode: str = "balanced",
    seed: int = 42,
    num_samples: int = 1,
    save_file_name: str = 'fashn_result'
    ):

    model_img = load_image(model_image)
    model_img = encode_img_to_base64(model_img)

    garment_img = load_image(garment_image)
    garment_img = encode_img_to_base64(garment_img)

    response = requests.post(
        "https://api.fashn.ai/v1/run",
        headers={"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"},
        json={
        "model_image": model_img,
        "garment_image": garment_img,
        "category": "tops",
        "num_samples": num_samples
        },
    )

    id = response.json()['id']

    response = None
    print("Generating virtual try-on...")

    while response is None or response.json()['status'] == 'processing':
        response = requests.get(
            f"https://api.fashn.ai/v1/status/{id}",
            headers={"Authorization": f"Bearer {bearer_token}"},
        )

        time.sleep(10)

    result = response.json()

    if result['status'] == 'completed':
        print("Completed.")

        print("Fetching and save results...")

        for i in range(num_samples):
            image_url = result['output'][i]

            fetch_and_save_image(image_url, f"data/tryon_results/{save_file_name}{i}.png")

            # image = Image.open(f"data/tryon_results/{save_file_name}{i}.png")
            
            # plt.imshow(image)
            # plt.axis('off')  
            # plt.show()

        return result['output']
    else:
        return result

if __name__ == "__main__":
    model_image = input("Enter the model image file name (with extension): ")
    garment_image = input("Enter the garment image file name (with extension): ")
    category = input("Enter the category ('tops' | 'bottoms' | 'one-pieces'): ")
    num_sample = int(input("Enter the number of samples to generate: "))

    model_image_path = f"data/model_images/{model_image}"
    garment_image_path = f"data/garment_images/{garment_image}"

    result = get_virtual_try_on(model_image_path, garment_image_path, category=category, mode='quality', num_samples=num_sample)