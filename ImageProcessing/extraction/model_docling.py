from PIL import Image
from docling.document_converter import DocumentConverter
import os


def extract_text_from_image_using_docling(image):
    # Convert the image to a temporary file if needed for Docling
    # If the image is a PIL Image, save it to a temporary file and convert
    if isinstance(image, Image.Image):
        image_path = "/tmp/temp_image.png"
        image.save(image_path)
    else:
        image_path = image  # Assume it's already a file path if it's not a PIL image

    # Use DocumentConverter from Docling
    converter = DocumentConverter()
    result = converter.convert(image_path)
    extracted_text = result.document.export_to_text()

    # Remove the temporary file after extraction
    if isinstance(image, Image.Image):  # Only remove the file if it was created
        if os.path.exists(image_path):
            os.remove(image_path)

    return extracted_text