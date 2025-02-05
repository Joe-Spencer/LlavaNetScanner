import os
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

category_colors = {
    'Images(.jpg, .png, etc.)': '#FF6B6B',
    'Videos(.mp4, .mov, etc.)': '#4ECDC4',
    'PDFs': '#45B7D1',
    'Audio(.mp3, .wav, etc.)': '#96CEB4',
    'Text(.txt)': '#FFBE0B',
    'Documents(.doc, .xls, etc.)': '#3D84A8',
    'Archives(.zip, .rar, etc.)': '#E76F51',
    'CAD(.dwg, .dxf, etc.)': '#9B5DE5',
    'Code': '#00B4D8',
    'Database': '#2A9D8F',
    'System': '#6C757D',
    'Outlook Backups': '#2EC4B6',
    'Photo Database': '#FF9F1C',
    'No Extension': '#C0C0C0'
}

def convert_size(size_bytes):
    return size_bytes / (1024 ** 3)  # Convert to GB

def get_file_category(ext, filename):  # Add filename parameter
    # Check for Outlook files first
        
    categories = {
        'Images(.jpg, .png, etc.)': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.raw', '.svg'],
        'Videos(.mp4, .mov, etc.)': ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.m4v', '.mpg', '.mpeg', '.3gp'],
        'PDFs': ['.pdf'],
        'Audio(.mp3, .wav, etc.)': ['.mp3', '.wav', '.wma', '.aac', '.flac', '.ogg', '.m4a'],
        'Text(.txt)': ['.txt'],
        'Documents(.doc, .xls, etc.)': ['.doc', '.docx', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'Archives(.zip, .rar, etc.)': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'CAD(.dwg, .dxf, etc.)': ['.dwg', '.dxf', '.dwf', '.rvt', '.rfa', '.ifc'],
        'Code': ['.py', '.js', '.html', '.css', '.cpp', '.h', '.java', '.php'],
        'Database': ['.db', '.sqlite', '.mdb', '.accdb'],
        'System': ['.sys', '.dll', '.exe', '.ini', '.config']
    }
    
    for category, extensions in categories.items():
        if ext.lower() in extensions:
            return category
    if 'outlook' in filename.lower():
        return 'Outlook Backups'
    if 'database' in filename.lower():
        return 'Database'
    if 'readme' in filename.lower() or 'license' in filename.lower():
        return 'Text(.txt)'
    if 'docker' in filename.lower():
        return 'Code'
    if filename.lower().startswith('.'):
        return filename
    return 'No Extension'

def analyze_directory(directory_path):
    # Get directory name from path
    dir_name = os.path.basename(os.path.normpath(directory_path))
    
    category_sizes = defaultdict(int)
    total_size = 0
    large_no_ext_files = []  # Track large files without extensions
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if file.startswith('.'):
                    ext = file
                    category = 'system'
                else:
                    ext = os.path.splitext(file)[1].lower() or 'no extension'
                    category = get_file_category(ext, file)  # Pass filename
                
                category_sizes[category] += size
                total_size += size
                
                # Track files >0.125GB without extension
                if ext == 'no extension':
                    print(file_path)
                    if size > ((1024 ** 3)*0.125):
                        large_no_ext_files.append((file_path, convert_size(size)))
                    
            except (OSError, FileNotFoundError):
                continue
    
    total_gb = convert_size(total_size)
    percentages = {}
    other_size = 0
    threshold = 0.5
    
    # Create labels with both percentage and GB
    labels = []
    sizes = []
    other_gb = 0.5
    
    # First pass to calculate total "other" size
    for category, size in category_sizes.items():
        percentage = (size / total_size) * 100
        if percentage < threshold:
            other_size += percentage
            other_gb += size
        else:
            size_gb = convert_size(size)
            percentages[category] = (percentage, size_gb)
    
    # Sort by percentage and create labels
    for category, (percentage, size_gb) in sorted(percentages.items(), 
                                           key=lambda x: x[1][0], 
                                           reverse=True):
        labels.append(f'{category} ({percentage:.1f}%, {size_gb:.2f} GB)')
        sizes.append(percentage)
    
    # Add other category at the end
    if other_size > 0:
        other_gb = convert_size(other_gb)
        labels.append(f'other: ({other_size:.1f}%, {other_gb:.2f} GB)')
        sizes.append(other_size)
    
    # Sort sizes in descending order for better visualization
    sorted_data = sorted(zip(sizes, labels), reverse=True)
    sizes, labels = zip(*sorted_data)
    
    # Create figure with a specific aspect ratio
    plt.figure(figsize=(12, 8))
    
    # Create custom labels that hide small percentages
    label_texts = []
    for size, label in zip(sizes, labels):
        if size < 3:
            label_texts.append('')  # Empty label for small slices
        else:
            label_texts.append(label)

    def get_category_from_label(label):
        # Extract the base category name before the percentage
        return label.split(' (')[0]

    # Create pie chart with enhanced styling
    patches, texts, autotexts = plt.pie(sizes, 
                                       labels=label_texts,  # Use modified labels
                                       autopct=lambda pct: f'{pct:.1f}%' if pct >= 3 else '',  # Hide small percentages
                                       startangle=90,
                                       pctdistance=0.85,
                                       explode=[0.05] * len(sizes),
                                       shadow=True,
                                       colors=[category_colors.get(get_category_from_label(label), '#C0C0C0') for label in labels])
    
    # Enhance the appearance of labels
    plt.setp(autotexts, size=8, weight="bold")
    plt.setp(texts, size=9)
    
    # Add a legend
    plt.legend(patches, labels, 
              title="File Types",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.title(f'{dir_name} Storage Distribution by File Type\nTotal Size: {total_gb:.2f} GB',
             pad=20,
             size=12,
             weight='bold')
             
    plt.axis('equal')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    print(f"\nTotal size: {total_gb:.2f} GB")
    print("\nFile type distribution:")
    for category, size in category_sizes.items():
        size_gb = convert_size(size)
        percentage = (size / total_size) * 100
        print(f"{category}: {percentage:.1f}% ({size_gb:.2f} GB)")
    
    # Print warning about large files without extensions
    if large_no_ext_files:
        print("\nWARNING: Large files (>1GB) found without extensions:")
        for file_path, size_gb in sorted(large_no_ext_files, key=lambda x: x[1], reverse=True):
            print(f"{file_path}: {size_gb:.2f} GB")
    
    plt.show()

if __name__ == "__main__":
    directory = input("Enter directory path to analyze: ")
    if os.path.exists(directory):
        analyze_directory(directory)
    else:
        print("Invalid directory path!")