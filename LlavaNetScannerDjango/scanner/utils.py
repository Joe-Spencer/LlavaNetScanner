import os
import pandas as pd
from datetime import datetime
from django.conf import settings
from django.utils.timezone import make_aware
import subprocess
import platform

# Add constant for cutoff date - make timezone aware
CUTOFF_DATE = make_aware(datetime(2023, 10, 1))

# Check for image files
def is_image_file(filename):
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    return filename.lower().endswith(image_extensions)

# Check for autocad files
def is_design_file(filename):
    design_extensions = ('.dwg', '.dxf')
    return filename.lower().endswith(design_extensions)

# Check for PDFs
def is_pdf_file(filename):
    return filename.lower().endswith('.pdf')

# Check for text files
def is_text_file(filename):
    text_extensions = ('.txt', '.doc', '.docx')
    return filename.lower().endswith(text_extensions)

# Check if the file is one of the valid file types
def is_valid_file(file_path):
    """Check if the file is valid and exists"""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return False
        
    filename = os.path.basename(file_path)
    if is_image_file(filename) or is_design_file(filename) or is_pdf_file(filename):
        return True
    return False

def open_file_location(path):
    """Open the folder containing the file in the system's file explorer"""
    try:
        if platform.system() == "Windows":
            # On Windows, use explorer and select the file
            subprocess.run(['explorer', '/select,', path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(['open', '-R', path])
        else:  # Linux
            subprocess.run(['xdg-open', os.path.dirname(path)])
        return True
    except Exception as e:
        return False 