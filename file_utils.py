import os
from typing import List, Optional
import requests
import numpy as np
import cv2
import base64
from PIL import Image

def list_files_in_directory(directory: str) -> List[str]:
    """List all files in a directory."""
    if not os.path.exists(directory):
        return []
    return sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])

def print_file_options(files: List[str], directory: str):
    """Print numbered list of files."""
    print(f"\nAvailable files in {directory}:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

def get_valid_file_input(directory: str) -> Optional[str]:
    """
    Get valid file input from user with numbered options.
    Returns the selected filename or None if user wants to exit.
    """
    while True:
        files = list_files_in_directory(directory)
        if not files:
            print(f"No files found in {directory}")
            return None
        
        print_file_options(files, directory)
        choice = input(f"Enter selection: ").strip()
        
        try:
            idx = int(choice)
            if 1 <= idx <= len(files):
                return files[idx - 1]
        except ValueError:
            pass
            
        print("\nInvalid selection. Please try again.")

def get_file_path(filename: str, directory: str) -> Optional[str]:
    """Get full path for a file if it exists."""
    file_path = os.path.join(directory, filename)
    return file_path if os.path.isfile(file_path) else None 

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