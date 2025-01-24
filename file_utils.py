import os
from typing import List, Optional

def list_files_in_directory(directory: str) -> List[str]:
    """List all files in a directory."""
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

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