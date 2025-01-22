import requests
import numpy as np
import cv2
import base64
from PIL import Image
import time
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

DIR_MODEL_IMAGES = "data/model_images"
DIR_GARMENT_IMAGES = "data/garment_images"
DIR_TRYON_RESULTS = "data/tryon_results"
# Load environment variables from .env file
load_dotenv()

# Get environment variables
bearer_token = os.getenv('FASHN_BEARER_TOKEN')

def load_image(file_name):
    """
    Loads an image from a file
    file_name: the file name of the image (with extension)
    """

    img = Image.open(file_name)
    img = img.convert("RGB")  # Ensure the image is in RGB format
    img.load()
    data = np.asarray(img, dtype="uint8")  # Change dtype to uint8
    return data

def encode_img_to_base64(img: np.array) -> str:
    """
    Encodes an image as a JPEG in Base64 format.
    img: the image to encode
    """
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
    """
    Fetches an image from a URL and saves it to a file
    url: the URL of the image
    filename: the file name to save the image (with extension)
    """

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
    save_file_name: str = 'fashn_result.png'
    ):
    """
    Generates a virtual try-on image with FASHN API
    model_image: the model image file name (with extension)
    garment_image: the garment image file name (with extension)
    category: the category of the garment ('tops' | 'bottoms' | 'one-pieces')
    nsfw_filter: whether to filter out NSFW images
    cover_feet: whether to cover the feet
    adjust_hands: whether to adjust the hands
    restore_background: whether to restore the background
    restore_clothes: whether to restore the clothes
    garment_photo_type: the type of garment photo ('auto' | 'model' | 'flat')
    long_top: whether the garment is a long top
    mode: the mode of the virtual try-on ('balanced' | 'quality' | 'speed')
    seed: the seed for the virtual try-on
    num_samples: the number of samples to generate
    save_file_name: the file name to save the results (with extension)
    """

    model_img = load_image(f"{DIR_MODEL_IMAGES}/{model_image}")
    model_img = encode_img_to_base64(model_img)

    garment_img = load_image(f"{DIR_GARMENT_IMAGES}/{garment_image}")
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

        save_file_name, save_file_name_extension = save_file_name.split('.')

        for i in range(num_samples):
            image_url = result['output'][i]

            save_file_path = f"{DIR_TRYON_RESULTS}/{save_file_name}{i}.{save_file_name_extension}"
            fetch_and_save_image(image_url, save_file_path)

            # image = Image.open(save_file_path)
            
            # plt.imshow(image)
            # plt.axis('off')  
            # plt.show()

        return result['output']
    else:
        print("Failed to generate virtual try-on.")
        return result

if __name__ == "__main__":
    model_image = input("Enter the model image file name (with extension): ")
    garment_image = input("Enter the garment image file name (with extension): ")
    category = input("Enter the category ('tops' | 'bottoms' | 'one-pieces'): ")
    num_sample = int(input("Enter the number of samples to generate: "))

    result = get_virtual_try_on(model_image, garment_image, category=category, mode='quality', num_samples=num_sample)