import os
import pandas as pd
from datetime import datetime
from image_describer import generate_description
from design_describer import describe_design
from pdf_describer import describe_pdf
from dotenv import load_dotenv

# Add constant for cutoff date
CUTOFF_DATE = datetime(2023, 10, 1)

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

#Check for text files
def is_text_file(filename):
    text_extensions = ('.txt', '.doc', '.docx')
    return filename.lower().endswith(text_extensions)

#Check if the file is one of the valid file types
def is_valid_file(filename):
    if is_image_file(filename) or is_design_file(filename) or is_pdf_file(filename):
        return True 

#Process the file and return the row of data
def process_file(file_path, directory):
    """Process a file and return its metadata and description"""
    try:
        relative_path = os.path.relpath(file_path, directory)
        path_parts = relative_path.split(os.sep)
        contractor = path_parts[0] if len(path_parts) >= 2 else 'unknown'
        project = path_parts[1] if len(path_parts) >= 3 else 'unknown'
        
        # Get the actual filename from the path
        filename = os.path.basename(file_path)
        
        # Get file description based on type
        description = ''
        if is_image_file(filename):
            description = generate_description(file_path, mode='detailed')
        elif is_design_file(filename):
            description = describe_design(file_path)
        elif is_pdf_file(filename):
            description = describe_pdf(file_path)
        else:
            description = 'Unknown file type'
            
        # Create result dictionary
        result = {
            'Filename': filename,
            'Path': file_path,
            'Contractor': contractor,
            'Project': project,
            'Description': description,
            'file_type': os.path.splitext(filename)[1].lower()
        }
        
        return result
        
    except Exception as e:
        print(f"Error in process_file: {str(e)}")
        # Return a basic result with error message
        return {
            'Filename': os.path.basename(file_path),
            'Path': file_path,
            'Contractor': 'unknown',
            'Project': 'unknown',
            'Description': f'Error processing file: {str(e)}',
            'file_type': os.path.splitext(file_path)[1].lower()
        }

def scan_files_in_directory(directory_path, db):
    """
    Scan files in directory and add them directly to database
    """
    data = []
    files_found = 0
    files_processed = 0
    files_skipped = 0
    
    print("\nStarting directory scan...")
    
    # Convert to absolute path to avoid any path resolution issues
    directory_path = os.path.abspath(directory_path)
    processed_paths = set()
    
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.abspath(os.path.join(root, filename))
            
            if file_path in processed_paths:
                continue
                
            files_found += 1
            print(f"\nFound file ({files_found}): {filename}")
            print(f"Full path: {file_path}")
            
            # Check if file is valid and newer than cutoff date
            if (is_valid_file(filename) and 
                os.path.getctime(file_path) > CUTOFF_DATE.timestamp()):
                
                # Check if file already exists in database
                existing_results = db.get_results({'file_path': file_path})
                if existing_results:
                    files_skipped += 1
                    print(f"⏭️  Skipping existing file: {filename}")
                    processed_paths.add(file_path)
                    continue
                
                print(f"🔍 Processing: {filename}")
                try:
                    result = process_file(file_path, directory_path)
                    db.add_scan_result(result)
                    files_processed += 1
                    print(f"✅ Added to database: {result['Filename']}")
                    processed_paths.add(file_path)
                    data.append(result)
                except Exception as e:
                    print(f"❌ Error processing {filename}: {str(e)}")
                    files_skipped += 1
                    processed_paths.add(file_path)
            else:
                files_skipped += 1
                print(f"⏭️  Skipping invalid or old file: {filename}")
                processed_paths.add(file_path)
    
    print(f"\nScan Complete!")
    print(f"Files found: {files_found}")
    print(f"Files processed: {files_processed}")
    print(f"Files skipped: {files_skipped}")
    
    return data

if __name__ == "__main__":
    directory_to_scan = r"your file path"
    output_csv_file = r'ouput.csv'
    df = pd.DataFrame(scan_files_in_directory(directory_to_scan))
    df.to_csv(output_csv_file, index=False)