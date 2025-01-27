from search import *
from post import *
from generate_virtual_tryon import *
from generate_model_image import *

if __name__ == "__main__":
    model_option = input("Do you want to generate a new model image? (y/n): ")

    if model_option == 'y':
        model_image_prompt = input("Enter the model image prompt: ")
        print_file_options(list_files_in_directory(DIR_MODEL_IMAGES), DIR_MODEL_IMAGES)
        model_filename = input("Enter the file name (with extension) to save the image: ")
        generate_image_flux(model_image_prompt, model_filename)
    else:
        print("Select model image:")
        model_filename = get_valid_file_input(DIR_MODEL_IMAGES)

    
    print("Select garment image:")
    garment_filename = get_valid_file_input(DIR_GARMENT_IMAGES)
    # category = input("Enter the category ('tops' | 'bottoms' | 'one-pieces'): ")
    num_sample = int(input("Enter the number of samples to generate (1-4): "))

    result = get_virtual_try_on(model_filename, garment_filename, save_filename=None, category="tops", mode='quality', num_samples=num_sample)
    print(result)

    post_tweet = input("Do you want to post a tweet? (y/n): ")
    if post_tweet == 'y':
        tweet_text = input("Enter the tweet text: ")
        print_file_options(list_files_in_directory(DIR_TRYON_RESULTS), DIR_TRYON_RESULTS)
        tweet_image_file_name = input("Enter the tweet image file name (with extension): ")
        create_tweet_with_media(tweet_text, f"{DIR_TRYON_RESULTS}/{tweet_image_file_name}")