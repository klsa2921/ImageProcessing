from extraction.model_pytesseract import extract_text_from_file_for_pytesseract
from extraction.model_easyocr import extract_text_from_file_using_easyocr
from extraction.model_docling import extract_text_from_image_using_docling

def extract_text_using_all_models(image):
    text = ''
    model_used = ''
    try:
        print("Extracting text using Tesseract...")
        text = extract_text_from_file_for_pytesseract(image)
        model_used = 'model1'
    except Exception as e:
        print(f"Error processing image with Tesseract (error: {str(e)}). Trying with EasyOCR...")
        try:
            
            text = extract_text_from_file_using_easyocr(image)
            model_used = 'model2'
        except Exception as e:
            
            print(f"Error processing image with EasyOCR (error: {str(e)}). Trying with Docling...")
            text = extract_text_from_image_using_docling(image)
            model_used = 'model3'
    
    return text, model_used


def extract_text_by_given_model(image, model):
    text = ''
    model_used = ''
    try:
        if model == 'Tesseract':
            print("Extracting text using Tesseract...")
            text = extract_text_from_file_for_pytesseract(image)
            model_used = 'model1'
        elif model == 'EasyOCR':
            print("Extracting text using EasyOCR...")
            text = extract_text_from_file_using_easyocr(image)
            model_used = 'model2'
        elif model == 'Docling':
            print("Extracting text using Docling...")
            text = extract_text_from_image_using_docling(image)
            model_used = 'model3'
        else:
            raise ValueError("Unsupported model specified.")
    except Exception as e:
        print(f"Error processing image with {model} (error: {str(e)}).")
    
    return text, model_used