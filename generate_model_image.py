from file_utils import *
from dotenv import load_dotenv
import time

DIR_MODEL_IMAGES = "data/model_images"

# def generate_image_flux(prompt, save_filename):
#     """
#     Generates an image using Flux.1-schnell model
#     prompt: the prompt for the image
#     save_filename: the file name to save the image (with extension)
#     """

#     client = Client("black-forest-labs/FLUX.1-schnell")

#     result = client.predict(
#         prompt=prompt,
#         seed=0,
#         randomize_seed=True,
#         width=1024,
#         height=1024,
#         num_inference_steps=4,
#         api_name="/infer"
#     )

#     image = Image.open(result[0])
#     image.save(f"{DIR_MODEL_IMAGES}/{save_filename}")

#     return image

load_dotenv()

def generate_image_flux(prompt, save_filename):
    """
    Generates an image using Flux.1-prod model
    prompt: the prompt for the image
    save_filename: the file name to save the image (with extension)
    """

    request = requests.post(
        'https://api.us1.bfl.ai/v1/flux-pro-1.1',
        headers={
            'accept': 'application/json',
            'x-key': os.environ.get("BFL_API_KEY"),
            'Content-Type': 'application/json',
        },
        json={
            'prompt': prompt,
            'width': 960,
            'height': 1440, # 2:3 aspect ratio, 1440 is the maximum input allowed
        },
    ).json()

    # print(request)

    request_id = request["id"]    

    while True:
        time.sleep(0.5)

        result = requests.get(
            'https://api.us1.bfl.ai/v1/get_result',
            headers={
                'accept': 'application/json',
                'x-key': os.environ.get("BFL_API_KEY"),
            },
            params={
                'id': request_id,
            },
        ).json()

        if result["status"] == "Ready":
            image_url = result['result']['sample']
            save_file_path = f"{DIR_MODEL_IMAGES}/{save_filename}"
            fetch_and_save_image(image_url, save_file_path)        
            print(f"Image saved to {save_file_path}")
            break
        else:
            print(f"Status: {result['status']}")    

    return save_file_path

if __name__ == "__main__":
    prompt = input("Enter the prompt for the image: ")
    print_file_options(list_files_in_directory(DIR_MODEL_IMAGES), DIR_MODEL_IMAGES)
    save_filename = input("Enter the file name (with extension) to save the image: ")
    generate_image_flux(prompt, save_filename)