#Generate Description of the image using Llava 7B, a vision model based on Llama, this is a good compromise between cost and accuracy
import ollama

def generate_description(image_path, mode='detailed'):
    try:
        # Set the prompt based on the mode
        content = 'Describe this image:'
        if mode == 'detailed':
            content = 'Describe this image using as much technical detail as possible:'
        elif mode == 'concise':
            content = 'Describe this image in simple terms:'
        elif mode == 'creative':
            content = 'Describe this image in a creative way:'
        else:
            content = 'Describe this image:'
        # format the message for Ollama
        messages = []
        message = {
            'role': 'user',
            'content': content,
            'images': [image_path]
        }
        messages.append(message)
        # Generate the response
        response = ollama.chat(model='llava', messages=messages)
        # format the response from Ollama
        response = response['message']['content']
        return response
    except Exception as e:
        return f"Error: {e}"