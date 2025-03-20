# LlavaNetScannerDjango

A Django-based web application for scanning and analyzing network files with AI-powered content description.

## Overview

LlavaNetScannerDjango is a modern web application that scans directories containing various file types (images, PDFs, CAD files) and uses AI to generate descriptions of file contents. It's designed to help organize and search through large collections of technical files, particularly in engineering or architectural contexts.

## Features

- **Directory Scanning**: Scan directories recursively to find relevant files
- **AI-Powered Description**: Uses Ollama with the Llava model to automatically generate descriptions of images
- **Basic descriptions for design files and PDFs**: Provides information about file properties
- **Customizable Description Depth**: Choose between detailed, concise, or creative descriptions
- **Filtering and Search**: Filter results by contractor, project, or file type
- **Data Visualization**: View statistics about scanned files with interactive charts
- **Export to CSV**: Export scan results for further analysis
- **Open File Locations**: Directly open file locations from the interface

## Requirements

- Python 3.8+
- Django 5.1+
- Pandas
- Plotly
- Matplotlib
- Numpy
- Ollama with Llava model
- Python-dotenv

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd NetworkScanner/DjangoRework
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r LlavaNetScannerDjango/requirements.txt
```

4. Install and set up Ollama locally:
   - Download from [Ollama.ai](https://ollama.ai)
   - Install Llava model: `ollama pull llava`

5. Navigate to the project directory:
```
cd LlavaNetScannerDjango
```

6. Apply database migrations:
```
python manage.py migrate
```

7. Run the development server:
```
python manage.py runserver
```

8. Access the application at http://127.0.0.1:8000/

## Usage

1. **Start a New Scan**:
   - Go to the "Scan" tab
   - Enter a directory path
   - Select a description mode (detailed, concise, creative)
   - Choose a cutoff date for file processing
   - Click "Start Scan"

2. **View Results**:
   - The "Database" tab shows all scanned files
   - Use the search and filter options to narrow down results
   - Click on file rows to see more details

3. **Export Data**:
   - Use the "Export to CSV" button to download results
   - Filtered results will be included in the export

4. **View Statistics**:
   - The "Dashboard" tab shows file statistics
   - View breakdowns by file type and contractor

## Troubleshooting

- If scanning doesn't work properly, test the Ollama service using the "Test Ollama Service" button
- Ensure the Llava model is installed in Ollama
- Check that the directories you're scanning exist and are accessible
- Look for error messages in the application logs

## License

[Your License Information]

## Credits

Developed by [Your Name/Organization] 