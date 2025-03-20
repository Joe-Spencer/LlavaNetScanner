import ollama
import os
import logging
from datetime import datetime

# Set up logger
logger = logging.getLogger(__name__)

def generate_image_description(image_path, mode='detailed'):
    """
    Generate a description of an image using different modes:
    - detailed: Technical and comprehensive description
    - concise: Brief, focused description
    - creative: More artistic/narrative description
    """
    try:
        logger.debug(f"Generating description for image: {image_path} with mode: {mode}")
        
        # Check if image exists
        if not os.path.exists(image_path):
            logger.error(f"Image file does not exist: {image_path}")
            return f"Error: Image file not found at {image_path}"
        
        # Set the prompt based on the mode
        prompts = {
            'detailed': 'Describe this image in detail, focusing on technical aspects, materials, construction elements, and architectural features. Include any relevant measurements, colors, or specifications visible.',
            
            'concise': 'Provide a brief, focused description of this image in 2-3 sentences, highlighting the main subject and key features.',
            
            'creative': 'Describe this image in a narrative style, focusing on the story it tells and the atmosphere it creates. Consider the mood, lighting, and overall composition.',
            
            # Default to detailed if mode not recognized
            'default': 'Describe this image in detail, focusing on technical aspects and key features.'
        }
        
        # Get appropriate prompt or fall back to default
        content = prompts.get(mode.lower(), prompts['default'])
        logger.debug(f"Using prompt: {content}")
        
        # Format the message for Ollama
        messages = [{
            'role': 'user',
            'content': content,
            'images': [image_path]
        }]
        
        # Generate the response
        logger.debug("Calling Ollama API with llava model")
        response = ollama.chat(model='llava', messages=messages)
        logger.debug(f"Received response from Ollama: {response}")
        
        # Format and clean up the response
        description = response['message']['content'].strip()
        
        # For concise mode, ensure response isn't too long
        if mode.lower() == 'concise' and len(description.split()) > 50:
            # Take first few sentences
            sentences = description.split('.')[:3]
            description = '. '.join(sentences) + '.'
            
        logger.debug(f"Returning description with length: {len(description)}")
        return description
        
    except Exception as e:
        logger.exception(f"Error generating image description: {str(e)}")
        return f"Error generating description: {str(e)}"

def describe_design(file_path):
    """Generate a description for CAD design files"""
    try:
        logger.debug(f"Describing design file: {file_path}")
        
        # For now, just return basic info about the design file
        # In a real implementation, you might use a CAD processing library
        filename = os.path.basename(file_path)
        file_type = os.path.splitext(filename)[1].lower()
        
        description = f"CAD design file ({file_type}). Contains blueprint or technical drawing. "
        description += "To view detailed contents, please open with appropriate CAD software."
        
        return description
    except Exception as e:
        logger.exception(f"Error describing design file: {str(e)}")
        return f"Error describing design file: {str(e)}"

def describe_pdf(file_path):
    """Generate a description for PDF files"""
    try:
        logger.debug(f"Describing PDF file: {file_path}")
        
        # Since PyMuPDF is having installation issues, we'll provide a simple description
        # based on file attributes
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        size_mb = round(file_size / (1024 * 1024), 2)
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        description = f"PDF Document: {filename}. Size: {size_mb} MB. "
        description += f"Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}. "
        description += "Full text extraction not available in this version."
        
        return description
            
    except Exception as e:
        logger.exception(f"Error describing PDF: {str(e)}")
        return f"Error describing PDF: {str(e)}" 