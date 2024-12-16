import os
import pandas as pd

#Define the kinds of image files we want to scan
def is_design_file(filename):
    image_extensions = ('.dwg', '.dxf')
    return filename.lower().endswith(image_extensions)

#Generate Description of the image using Llava 7B, a vision model based on Llama, this is a good compromise between cost and accuracy
def describe_design(design_path):
    try:
        # format the message for Ollama, including a message content apporopriate for Llava
        if "rail" in design_path.lower():
            response = "Rail"
        elif "hood" in design_path.lower():
            response = "Hood"
        elif "stair" in design_path.lower():
            response = "Stair"
        elif "gate" in design_path.lower():
            response = "Gate"
        elif "light" in design_path.lower():
            response = "Light"
        elif "fence" in design_path.lower():  
            response = "Fence"
        elif "door" in design_path.lower():
            response = "Door"
        elif "desk" in design_path.lower():
            response = "Window"
        elif "iron" in design_path.lower():
            response = "Iron"
        else:
            response = "Miscellaneous"
        if "int" in design_path.lower():
            response = "Interior " + response
        elif "ext" in design_path.lower():   
            response = "Exterior " + response
        if '.dwg' in design_path.lower():
            response = response + " Drawing"
        elif '.dxf' in design_path.lower():
            response = response + " CAM File"
        return response

    except Exception as e:
        return f"Error: {e}"
