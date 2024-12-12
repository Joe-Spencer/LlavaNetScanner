import os
import pandas as pd

#Define the kinds of image files we want to scan
def is_design_file(filename):
    image_extensions = ('.dwg', '.dxf')
    return filename.lower().endswith(image_extensions)

#Generate Description of the image using Llava 7B, a vision model based on Llama, this is a good compromise between cost and accuracy
def generate_description(image_path):
    try:
        # format the message for Ollama, including a message content apporopriate for Llava
        if "rail" in image_path.lower():
            response = "Rail"
        elif "hood" in image_path.lower():
            response = "Hood"
        elif "stair" in image_path.lower():
            response = "Stair"
        elif "gate" in image_path.lower():
            response = "Gate"
        elif "light" in image_path.lower():
            response = "Light"
        else:
            response = "Miscellaneous"
        if "int" in image_path.lower():
            response = "Interior " + response
        elif "ext" in image_path.lower():   
            response = "Exterior " + response
        if '.dwg' in image_path.lower():
            response = response + " Drawing"
        elif '.dxf' in image_path.lower():
            response = response + " CAM File"
        return response

    except Exception as e:
        return f"Error: {e}"

#Scan all the images in a directory, including images in subdirectories
def scan_images_in_directory(directory):
    data = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if is_design_file(filename):
                print("filename",filename)
                file_path = os.path.join(root, filename)
                # generate a description of the image using an LLM
                # Extract contractor and project names from the path
                relative_path = os.path.relpath(file_path, directory)
                path_parts = relative_path.split(os.sep)
                contractor = path_parts[0] if len(path_parts) >= 2 else 'unknown'
                project = path_parts[1] if len(path_parts) >= 3 else 'unknown'
                description = generate_description(file_path)
                # format the data
                data.append({
                    'Filename': filename,
                    'Path': file_path,
                    'Contractor': contractor,
                    'Project': project,
                    'Category': description
                })
    # create a pandas dataframe
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    directory_to_scan = r'ScannedDirectory'
    output_csv_file = r'Designs.csv'
    df = scan_images_in_directory(directory_to_scan)
    df.to_csv(output_csv_file, index=False)