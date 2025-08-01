import os

def validate_file_path(file_path: str):
    if not os.path.isfile(file_path):
        raise ValueError(f"Invalid file path: {file_path}")
