import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import ollama

#Define the kinds of image files we want to scan
def is_image_file(filename):
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    return filename.lower().endswith(image_extensions)

#Generate Description of the image using Llava 7B, a vision model based on Llama, this is a good compromise between cost and accuracy
def generate_description(image_path):
    try:
        # format the message for Ollama, including a message content apporopriate for Llava
        messages = []
        message = {
            'role': 'user',
            'content': 'Describe this image using as much technical detail as possible:',
            'images': [image_path]
        }
        messages.append(message)
        response = ollama.chat(model='llava', messages=messages)
        # format the response from Ollama
        response = response['message']['content']
        print(response)
        return response

    except Exception as e:
        return f"Error: {e}"

#Process the file and return the metadata
def process_file(file_path, directory):
    relative_path = os.path.relpath(file_path, directory)
    path_parts = relative_path.split(os.sep)
    contractor = path_parts[0] if len(path_parts) >= 2 else 'unknown'
    project = path_parts[1] if len(path_parts) >= 3 else 'unknown'
    description = generate_description(file_path)
    return {
        'Filename': os.path.basename(file_path),
        'Path': file_path,
        'Contractor': contractor,
        'Project': project,
        'Description': description
    }

#Scan the images in the directory. If a checkpoint file exists, start from there
def scan_images_in_directory(directory, checkpoint_file):
    # Load existing data if checkpoint file exists
    if os.path.exists(checkpoint_file):
        df = pd.read_csv(checkpoint_file)
        processed_files = set(df['Path'].tolist())
    else:
        df = pd.DataFrame(columns=['Filename', 'Path', 'Contractor', 'Project', 'Description'])
        processed_files = set()

    data = df.to_dict('records')
    with ProcessPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if is_image_file(filename) and file_path not in processed_files:
                    futures.append(executor.submit(process_file, file_path, directory))
        
        for future in as_completed(futures):
            result = future.result()
            data.append(result)
            # Save progress to checkpoint file periodically
            if len(data) % 100 == 0:
                pd.DataFrame(data).to_csv(checkpoint_file, index=False)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    directory_to_scan = r'directory to scan'
    output_csv_file = r'Images_Finished.csv'
    checkpoint_file = r'Images_checkpoint.csv'
    df = scan_images_in_directory(directory_to_scan, checkpoint_file)
    df.to_csv(output_csv_file, index=False)