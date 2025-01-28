from PIL import Image
import os
import json
import fitz
from extraction.extract import extract_text_by_given_model, extract_text_using_all_models

def process_file(file_path, model):
    # Extract file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    result = {}

    if file_extension == '.pdf':
        # Convert PDF to images using PyMuPDF
        pdf_document = fitz.open(file_path)
        result['pages'] = []

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # img_np = np.array(img) ## 
            if model == 'default':
                output, model_used = extract_text_using_all_models(img)
            else:
                output, model_used = extract_text_by_given_model(img, model)
            result['pages'].append({
                'page_number': page_number + 1,
                'model_used': model_used,
                'extracted_text': output
            })

    elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        # Handle image files directly
        img = Image.open(file_path)
        if model == 'default':
            output, model_used = extract_text_using_all_models(img)
        else:
            output, model_used = extract_text_by_given_model(img, model)
        result['image_path'] = file_path
        result['model_used'] = model_used
        result['extracted_text'] = output

    else:
        raise ValueError("Unsupported file type. Only image and PDF files are supported.")

    return json.dumps(result, indent=4, ensure_ascii=False)