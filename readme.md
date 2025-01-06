# LlavaNetScanner

## Project Overview

LlavaNetScanner is an AI swarm that uses multiple Agents to analyze various design files, such as images, PDFs and DWG files. The primary goal of the project is to generate detailed descriptions of these files and organize them based on their attributes. This helps in managing and retrieving design files efficiently.

## Key Features

1. **Automated Scanning**: The project includes scripts that automatically scan directories for design files.
2. **File Analysis**: Different AI Agents are used to Analyze different types of files.
3. **Description Generation**: The Agent generates a detailed description of each file based on their content and metadata.
4. **Metadata Management**: Maintains metadata about the files, such as file paths, contractors, projects, and categories.
5. **Output Organization**: The generated descriptions and metadata are organized in CSV files for easy access and management.

## Components

### Scripts

- **ImageScanner.py**: This Agent uses Llava to analyze image files, generating descriptions based on their content. 
- **pdf_describer.py**: This Agent processes pdf files. If text can be pulled directly from the pdf then Llama3 is used to analyze the text and metadata. If text cannot be pulled from the pdf then it is converted to an image and Llava is used to analyze the file.
- **DWGScanner.py**: This script processes DWG files, generating descriptions based on their name alone. A future update will add in-depth dwg analysis


### Data Files

- **checkpoint.csv**: A CSV file containing descriptions for all the files scanned so far. For larger directories this system may take several days to execute so this file allows the system to pick up from where it left off if there is a crash or power failure.

## How It Works

1. **File Placement**: Users place their design files in the appropriate directories.
2. **Swarm Execution**: Users run the `NetScanner.py` script to start up the swarm
3. **Description Generation**: The Agents in the swarm generate descriptions based on the content and metadata of the files.
4. **CSV Update**: The generated descriptions and metadata are saved in the `checkpoint.csv` file until all files in the directory have been scanned and then the results are saved to `output.csv`

## Usage

To use the LlavaNetScanner, follow these steps:

1. Install Ollama using "pip install ollama"
2. Ensure you have Llama3 and Llava using "Ollama run Llava" and "Ollama run Llama3"
2. Place your design files in the appropriate directories.
3. Run the `NetScanner.py` script to start up the swarm
4. Check the `checkpoint.csv` and `output.csv` files for the processed metadata and descriptions.

## Notes

This is a work in progress with many features yet to come.

By default the swarm uses Llava for images and Llama3 for text but can easily be modified to use any model supported by Ollama. 

Currently prompts are designed to produce highly detailed descriptions. If you want more concise descriptions change the prompts from something like "Describe this pdf using as much technical detail as possible" to something more like "Describe this pdf as concisely as possible".

If you need help or have new features you want to see added don't hesitate to create an issue!

## License

This project is licensed under the GNU General Public License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

