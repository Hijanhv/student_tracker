"""
File handling utilities
"""
import os

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)
