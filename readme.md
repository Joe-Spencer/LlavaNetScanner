# LlavaNetScanner

## Project Overview

LlavaNetScanner is an AI-enabled swarm that utilizes multiple agents to analyze various design files (e.g., images, PDFs, DWG/DXF files). The project automates file scanning, generates detailed descriptions based on file content and metadata, and organizes the results into a database and CSV files. A web-based interface, built with Streamlit, allows you to view, filter, and manage the scanned data interactively.

## Key Features

1. **Automated Scanning**: The system automatically scans directories for supported design files.
2. **File Analysis & Description**: 
   - **Images**: Analyzed via Llava to generate detailed, concise, or creative descriptions.
   - **PDFs**: Processed by Llama3 (when text is extractable) or converted and analyzed via Llava.
   - **CAD Files**: DWG/DXF file names are parsed for basic description, with plans for future in-depth analysis.
3. **Metadata Management**: Extracts and manages metadata including file paths, contractors, projects, file sizes, and timestamps.
4. **Database Integration**: Stores scan results in an SQLite database and includes utilities for migrating data to CSV or PostgreSQL.
5. **Interactive Streamlit Interface**: View database contents, apply filters, visualize data distributions, and initiate new directory scans via an intuitive web UI.
6. **Additional Utilities**:
   - **CSV to PostgreSQL Migration**: Migrate CSV data to a PostgreSQL database.
   - **File Storage Analysis**: Use the netgrapher tool to analyze storage usage by file type.

## Components

- **app.py**: The main Streamlit application that provides an interactive UI to view the database, visualize statistics, and scan new directories.
- **NetScanner.py**: Handles file scanning and processing—delegating tasks based on file type.
- **image_describer.py**: Generates image descriptions using Llava.
- **design_describer.py**: Provides basic descriptions for CAD files (.dwg, .dxf) based on file name cues.
- **pdf_describer.py**: Processes and describes PDF files.
- **database.py**: Manages the SQLite database that stores scan results.
- **csv_to_postgres.py**: Script to migrate CSV data into a PostgreSQL database.
- **migrate_csv_to_db.py**: Utility to migrate existing CSV data into the local database.
- **netgrapher.py**: Analyzes a directory's file distribution and visualizes storage usage with a pie chart.
- **LICENSE**: GNU General Public License.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd LlavaNetScanner
   ```

2. **Install Dependencies**:  
   Ensure you have Python 3.7+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   *If a `requirements.txt` file is not provided, manually install the required packages:*
   ```bash
   pip install streamlit pandas plotly psycopg2 matplotlib numpy python-dotenv ollama
   ```

3. **Set Up Models**:
   - Install Ollama: `pip install ollama`
   - Ensure Llava and Llama3 models are available by running:
     ```bash
     Ollama run Llava
     Ollama run Llama3
     ```

## Usage

### Running the Interactive Web Interface

    The primary interface is built with Streamlit. To start the application, run:

    ```bash
     streamlit run app.py --server.port 8502 --server.address localhost
     ```

