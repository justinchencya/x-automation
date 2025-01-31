from datetime import datetime
from dotenv import load_dotenv
import os
import time
from file_utils import *

DIR_MODEL_IMAGES = "data/model_images"
DIR_GARMENT_IMAGES = "data/garment_images"
DIR_TRYON_RESULTS = "data/tryon_results"

# Load environment variables from .env file
load_dotenv()

# Get environment variables
bearer_token = os.getenv('FASHN_BEARER_TOKEN')

def get_virtual_try_on(
    model_filename: str,
    garment_filename: str,
    save_filename: str,
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
    num_samples: int = 1
    ):
    """
    Generates a virtual try-on image with FASHN API
    model_filename: the model image file name (with extension)
    garment_filename: the garment image file name (with extension)
    save_filename: the file name to save the results (with extension)
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
    """

    model_image = load_image(f"{DIR_MODEL_IMAGES}/{model_filename}")
    model_image = encode_img_to_base64(model_image)

    garment_image = load_image(f"{DIR_GARMENT_IMAGES}/{garment_filename}")
    garment_image = encode_img_to_base64(garment_image)

    # Create default save file name if not provided
    if save_filename is None:
        model_name = model_filename.split('.')[0]
        garment_name = garment_filename.split('.')[0]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_filename = f"{model_name}_{garment_name}_{timestamp}.png"
        print(f"Save file name: {save_filename}")

    try:    
        response = requests.post(
            "https://api.fashn.ai/v1/run",
            headers={"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"},
            json={
                "model_image": model_image,
                "garment_image": garment_image,
                "category": category,
                "num_samples": num_samples,
                "nsfw_filter": nsfw_filter,
                "cover_feet": cover_feet,
                "adjust_hands": adjust_hands,
                "restore_background": restore_background,
                "restore_clothes": restore_clothes,
                "garment_photo_type": garment_photo_type,
                "long_top": long_top,
                "mode": mode,
                "seed": seed
            },
        )

        id = response.json()['id']
    except Exception as e:
        print("Error: Failed to generate virtual try-on.")
        print(f"Error: {e}")
        return None

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

        if num_samples == 1:
            image_url = result['output'][0]
            save_file_path = f"{DIR_TRYON_RESULTS}/{save_filename}"
            fetch_and_save_image(image_url, save_file_path)
        else:
            for i in range(num_samples):
                image_url = result['output'][i]

                save_file_path = f"{DIR_TRYON_RESULTS}/{save_filename.split('.')[0]}_{i}.{save_filename.split('.')[1]}"
                fetch_and_save_image(image_url, save_file_path)

        return result['output']
    else:
        print("Failed to generate virtual try-on.")
        print(response)
        return result

if __name__ == "__main__":
    print("Select model image:")
    model_filename = get_valid_file_input(DIR_MODEL_IMAGES)
    print("Select garment image:")
    garment_filename = get_valid_file_input(DIR_GARMENT_IMAGES)
    # category = input("Enter the category ('tops' | 'bottoms' | 'one-pieces'): ")
    num_sample = int(input("Enter the number of samples to generate (1-4): "))

    result = get_virtual_try_on(model_filename, garment_filename, save_filename=None, category="tops", mode='quality', num_samples=num_sample, seed=np.random.randint(0,100))