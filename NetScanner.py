import os
import pandas as pd
from image_describer import generate_description
from design_describer import describe_design
from pdf_describer import describe_pdf

#Check for image files
def is_image_file(filename):
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    return filename.lower().endswith(image_extensions)

#Check for autocad files
def is_design_file(filename):
    design_extensions = ('.dwg', '.dxf')
    return filename.lower().endswith(design_extensions)

#Check for PDFs
def is_pdf_file(filename):
    return filename.lower().endswith('.pdf')

#Check if the file is one of the valid file types
def is_valid_file(filename):
    if is_image_file(filename) or is_design_file(filename) or is_pdf_file(filename):
        return True 

#Process the file and return the row of data
def process_file(file_path, directory):
    relative_path = os.path.relpath(file_path, directory)
    path_parts = relative_path.split(os.sep)
    contractor = path_parts[0] if len(path_parts) >= 2 else 'unknown'
    project = path_parts[1] if len(path_parts) >= 3 else 'unknown'
    if is_image_file(file_path):
        description = generate_description(file_path, mode='detailed')
    elif is_design_file(file_path):
        description = describe_design(file_path)
    elif is_pdf_file(file_path):
        description = describe_pdf(file_path)
    else:
        description = 'what is this?'
    return {
        'Filename': os.path.basename(file_path),
        'Path': file_path,
        'Contractor': contractor,
        'Project': project,
        'Description': description
    }

def scan_files_in_directory(directory, checkpoint_file):
    # Load existing data if checkpoint file exists
    if os.path.exists(checkpoint_file):
        df = pd.read_csv(checkpoint_file)
        processed_files = set(df['Path'].tolist())
        print(f"Resuming from {checkpoint_file}")
    else:
        df = pd.DataFrame(columns=['Filename', 'Path', 'Contractor', 'Project', 'Description'])
        processed_files = set()
    data = df.to_dict('records')
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if is_valid_file(filename) and file_path not in processed_files:
                result = process_file(file_path, directory)
                data.append(result)
                # Save progress to checkpoint file
                pd.DataFrame(data).to_csv(checkpoint_file, index=False)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    directory_to_scan = r"Examples"
    output_csv_file = r'ouput.csv' 
    checkpoint_file = r'checkpoint.csv'
    df = scan_files_in_directory(directory_to_scan, checkpoint_file)
    df.to_csv(output_csv_file, index=False)