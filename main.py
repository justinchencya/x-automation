from search import *
from post import *
from generate_virtual_tryon import *
from generate_model_image import *

if __name__ == "__main__":
    print_file_options(list_files_in_directory(DIR_MODEL_IMAGES), DIR_MODEL_IMAGES)
    model_filename = input("Enter the model image file name (with extension): ")
    try:
        model_image_file_path = get_file_path(model_filename, DIR_MODEL_IMAGES)
        assert model_image_file_path is not None
    except:
        print("Model image not found. Creating new model image...")
        model_image_prompt = input("Enter the model image prompt: ")
        generate_image_flux(model_image_prompt, model_filename)

    print_file_options(list_files_in_directory(DIR_GARMENT_IMAGES), DIR_GARMENT_IMAGES)
    garment_filename = input("Enter the garment image file name (with extension): ")
    category = input("Enter the category ('tops' | 'bottoms' | 'one-pieces'): ")
    num_sample = int(input("Enter the number of samples to generate (1-4): "))
    # print_file_options(list_files_in_directory(DIR_TRYON_RESULTS), DIR_TRYON_RESULTS)
    # save_filename = input("Enter the file name to save the results (with extension): ")

    result = get_virtual_try_on(model_filename, garment_filename, save_filename=None, category=category, mode='quality', num_samples=num_sample)
    print(result)

    post_tweet = input("Do you want to post a tweet? (y/n): ")
    if post_tweet == 'y':
        tweet_text = input("Enter the tweet text: ")
        print_file_options(list_files_in_directory(DIR_TRYON_RESULTS), DIR_TRYON_RESULTS)
        tweet_image_file_name = input("Enter the tweet image file name (with extension): ")
        create_tweet_with_media(tweet_text, f"{DIR_TRYON_RESULTS}/{tweet_image_file_name}")