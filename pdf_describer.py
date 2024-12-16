import ollama
import fitz

def describe_pdf(pdf_path):
    seed="heirloom"
    seed=int(seed.encode('utf-8').hex(), 16)
    try:
        messages = []
        # Extract text from PDF using fitz
        with fitz.open(pdf_path) as doc:
            pdfContent = ""
            for page in doc:
                pdfContent += page.get_text()
        
        # If no text is extracted from the PDF, ask ollama to describe the PDF based on the name and file path
        if(pdfContent == ""):
            with fitz.open(pdf_path) as doc:
                page = doc.load_page(0)
                pix = page.get_pixmap()
                image_path = f"page.png"
                pix.save(image_path)
            message = {
                'role': 'user',
                'content': "Text could not be extracted from the PDF named: " + pdf_path + " so we have converted it to an image, please describe the pdf",
                'images': [image_path]
            }
            model='llava'
        
        # If text is extracted from the PDF, ask ollama to describe the PDF based on the content
        else:       
            message = {
                'role': 'user',
                'content': "Describe this pdf using as much technical detail as possible: " + pdf_path + "pdf content: " + pdfContent + "/end of pdf content",
            }
            model='Llama3'

        # Get response from Ollama
        messages.append(message)
        response = ollama.chat(
            model=model, 
            messages=messages,
            options={'seed': seed})
        
        # format the response from Ollama
        response = response['message']['content']
        return response

    except Exception as e:
        return f"Error: {e}"