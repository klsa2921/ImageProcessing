# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (tesseract-ocr, poppler-utils, etc.)
RUN apt-get update && \
    apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ara \
    poppler-utils \
    sudo && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    Flask \
    pytesseract \
    pillow \
    docling \
    pdf2image \
    easyocr \
    pymupdf \
    werkzeug

# Copy the local project files into the container
COPY . /app

# Expose the port that Flask will run on
EXPOSE 11200

CMD ["python", "main.py"]
