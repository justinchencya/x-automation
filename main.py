from search import *
from post import *
from generate_virtual_tryon import *
from generate_model_image import *

if __name__ == "__main__":
    model_image_prompt = input("Enter the model image prompt: ")
    model_image = input("Enter the model image name (with extension): ")
    generate_image_flux(model_image_prompt, model_image)

    garment_image = input("Enter the garment image name (with extension): ")
    category = input("Enter the category ('tops' | 'bottoms' | 'one-pieces'): ")
    num_sample = int(input("Enter the number of samples to generate: "))
    save_file_name = input("Enter the file name to save the results (with extension): ")

    result = get_virtual_try_on(model_image, garment_image, category=category, mode='quality', num_samples=num_sample, save_file_name=save_file_name)
    print(result)