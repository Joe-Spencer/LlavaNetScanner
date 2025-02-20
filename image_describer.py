#Generate Description of the image using Llava 7B, a vision model based on Llama, this is a good compromise between cost and accuracy
import ollama

def generate_description(image_path, mode='detailed'):
    """
    Generate a description of an image using different modes:
    - detailed: Technical and comprehensive description
    - concise: Brief, focused description
    - creative: More artistic/narrative description
    """
    try:
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
        
        # Format the message for Ollama
        messages = [{
            'role': 'user',
            'content': content,
            'images': [image_path]
        }]
        
        # Generate the response
        response = ollama.chat(model='llava', messages=messages)
        
        # Format and clean up the response
        description = response['message']['content'].strip()
        
        # For concise mode, ensure response isn't too long
        if mode.lower() == 'concise' and len(description.split()) > 50:
            # Take first few sentences
            sentences = description.split('.')[:3]
            description = '. '.join(sentences) + '.'
            
        return description
        
    except Exception as e:
        return f"Error generating description: {str(e)}"

if __name__ == "__main__":
    # Test the different modes
    test_image = "path/to/test/image.jpg"
    
    print("Detailed description:")
    print(generate_description(test_image, mode='detailed'))
    print("\nConcise description:")
    print(generate_description(test_image, mode='concise'))
    print("\nCreative description:")
    print(generate_description(test_image, mode='creative'))