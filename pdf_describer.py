import ollama
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Warning: PyMuPDF not installed. PDF text extraction will be limited.")
    fitz = None

def describe_pdf(pdf_path):
    seed="heirloom"
    seed=int(seed.encode('utf-8').hex(), 16)
    try:
        messages = []
        
        if fitz is None:
            # If PyMuPDF is not available, just analyze the PDF based on filename
            message = {
                'role': 'user',
                'content': f"Describe this PDF based on its filename: {pdf_path}"
            }
            model = 'Llama3'
        else:
            # Extract text from PDF using fitz
            try:
                with fitz.open(pdf_path) as doc:
                    pdfContent = ""
                    for page in doc:
                        pdfContent += page.get_text()
                
                # If no text is extracted from the PDF, use image-based analysis
                if not pdfContent.strip():
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
                    model = 'llava'
                else:
                    message = {
                        'role': 'user',
                        'content': "Describe this pdf using as much technical detail as possible: " + pdf_path + "pdf content: " + pdfContent + "/end of pdf content",
                    }
                    model = 'Llama3'
            except Exception as e:
                # If PDF processing fails, fallback to filename-based analysis
                message = {
                    'role': 'user',
                    'content': f"Error processing PDF. Describe based on filename: {pdf_path}"
                }
                model = 'Llama3'

        # Get response from Ollama
        messages.append(message)
        response = ollama.chat(
            model=model, 
            messages=messages,
            options={'seed': seed})
        
        return response['message']['content']

    except Exception as e:
        return f"Error: {e}"