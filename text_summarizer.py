import ollama

def describe_text(file_path):
    seed="heirloom"
    seed=int(seed.encode('utf-8').hex(), 16)
    try:
        # Read text file content
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        
        # If no text content found
        if not text_content.strip():
            return "No text content found in document"

        # Prepare message for Ollama
        message = {
            'role': 'user',
            'content': f"Summarize this text document: {file_path}\nContent: {text_content}\n/end of content"
        }

        # Get response from Ollama
        response = ollama.chat(
            model='Llama3',
            messages=[message]
        )
        
        return response['message']['content']

    except Exception as e:
        return f"Error reading text file: {str(e)}"