# LlavaNetScanner

## Project Overview

The LlavaNetScanner project is designed to automate the process of scanning and processing various design files, such as images and DWG files. The primary goal of the project is to generate detailed descriptions of these files and organize them based on their attributes. This helps in managing and retrieving design files efficiently.

## Key Features

1. **Automated Scanning**: The project includes scripts that automatically scan directories for design files.
2. **File Processing**: It processes different types of design files, including images and DWG files, to extract relevant information.
3. **Description Generation**: The project generates detailed descriptions of the files based on their content and metadata.
4. **Metadata Management**: It maintains metadata about the files, such as file paths, contractors, projects, and categories.
5. **Output Organization**: The generated descriptions and metadata are organized in CSV files for easy access and management.

## Components

### Scripts

- **ImageScanner.py**: This script processes image files, generating descriptions based on their content. It uses the file path to determine the type of image and generates a corresponding description.
- **DWGScanner.py**: This script processes DWG files, generating descriptions based on their content. It uses the file path to determine the type of drawing and generates a corresponding description.

### Data Files

- **Designs.csv**: A CSV file containing metadata about various design files, including their paths, contractors, projects, and categories.
- **lastoutput.csv**: A CSV file containing the latest output from the LlavaNetScanner, including descriptions of images and files processed.

## How It Works

1. **File Placement**: Users place their design files in the appropriate directories.
2. **Script Execution**: Users run the `ImageScanner.py` and `DWGScanner.py` scripts to process the files.
3. **Description Generation**: The scripts generate descriptions based on the content and metadata of the files.
4. **Metadata Update**: The generated descriptions and metadata are saved in the `Designs.csv` and `lastoutput.csv` files.

## Usage

To use the LlavaNetScanner, follow these steps:

1. Place your design files in the appropriate directories.
2. Run the `ImageScanner.py` and `DWGScanner.py` scripts to process the files and generate descriptions.
3. Check the `Designs.csv` and `lastoutput.csv` files for the processed metadata and descriptions.

## License

This project is licensed under the GNU General Public License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

