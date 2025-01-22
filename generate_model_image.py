from PIL import Image
from gradio_client import Client
import matplotlib.pyplot as plt

DIR_MODEL_IMAGES = "data/model_images"

def generate_image_flux(prompt, save_file_name):
    """
    Generates an image using Flux.1-schnell model
    prompt: the prompt for the image
    save_file_name: the file name to save the image (with extension)
    """

    client = Client("black-forest-labs/FLUX.1-schnell")

    result = client.predict(
        prompt=prompt,
        seed=0,
        randomize_seed=True,
        width=1024,
        height=1024,
        num_inference_steps=4,
        api_name="/infer"
    )

    image = Image.open(result[0])
    # plt.imshow(image)
    # plt.axis('off')  
    # plt.show()
    image.save(f"{DIR_MODEL_IMAGES}/{save_file_name}")

    return image

if __name__ == "__main__":
    prompt = input("Enter the prompt for the image: ")
    save_file_name = input("Enter the file name (with extension) to save the image: ")
    generate_image_flux(prompt, save_file_name)