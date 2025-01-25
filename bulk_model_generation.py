from generate_model_image import *
import random

if __name__ == "__main__":
    gender = ['male', 'female']
    age = ['young']
    body_type = ['athletic', 'curvy', 'petite']
    ethnicity = ['asian', 'black', 'caucasian', 'hispanic']
    hair_color = ['black', 'blonde', 'brown', 'gray']
    pose = ['standing']
    background = ['studio']
    pant_color = ['black', 'white', 'blue', 'red', 'green', 'yellow', 'purple', 'orange', 'gray', 'brown']

    # Number of combinations to generate
    num_combinations = int(input("Enter number of combinations to generate: "))
    
    print("Type of shots: 1. front, 2. back")
    direction = input("Enter the type of shots: ")

    for _ in range(num_combinations):
        # Randomly select one value from each parameter list
        selected_direction = 'front' if direction == '1' else 'back'
        selected_gender = random.choice(gender)
        selected_age = random.choice(age)
        selected_body_type = random.choice(body_type)
        selected_ethnicity = random.choice(ethnicity)
        selected_hair = random.choice(hair_color)
        selected_pose = random.choice(pose)
        selected_background = random.choice(background)
        selected_pant = random.choice(pant_color)

        # Create structured prompt
        if selected_direction == 'front':
            additional_prompt = "facing the camera"
        else:
            additional_prompt = "facing away from the camera"
        
        if selected_hair == 'blonde':
            selected_ethnicity = 'caucasian'

        prompt = f"A {selected_direction} shot of a {selected_age} {selected_ethnicity} {selected_gender} model with {selected_hair} hair and {selected_body_type} build, {selected_pose} in a {selected_background}, {additional_prompt}. Professional photoshoot, wearing black t-shirt and {selected_pant} pants."

        # Create systematic filename
        filename = f"ai_model_{selected_direction}_{selected_gender}_{selected_age}_{selected_body_type}_{selected_ethnicity}_{selected_hair}_{selected_pose}_{selected_background}_{selected_pant}.png"

        print(f"\nGenerating image with prompt: {prompt}")
        print(f"Saving as: {filename}")

        # Generate the image
        generate_image_flux(prompt, filename)