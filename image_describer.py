#Generate Description of the image using Llava 7B, a vision model based on Llama, this is a good compromise between cost and accuracy
import ollama

def generate_description(image_path):
    try:
        # format the message for Ollama, including a message content apporopriate for Llava
        messages = []
        message = {
            'role': 'user',
            'content': 'Describe this image using as much technical detail as possible:',
            'images': [image_path]
        }
        messages.append(message)
        response = ollama.chat(model='llava', messages=messages)
        # format the response from Ollama
        response = response['message']['content']
        return response

    except Exception as e:
        return f"Error: {e}"