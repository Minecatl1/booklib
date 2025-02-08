import os
import json
import  fitz # PyMuPDF
from PIL import Image
import subprocess

def convert_pdf_to_flipbook(pdf_path):
    output_folder = os.path.splitext(pdf_path)[0]
    os.makedirs(output_folder, exist_ok=True)
    subprocess.run(['pdf2htmlEX', '--zoom', '1.3', '--dest-dir', output_folder, pdf_path])
    return output_folder

def extract_first_page_as_image(pdf_path):
    doc = fitz.open(pdf_path)
    first_page = doc.load_page(0)  # Load the first page
    pix = first_page.get_pixmap()
    image_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page1.png"
    image_path = os.path.join('books', 'images', image_name)
    
    # Save the image
    pix.save(image_path)
    
    return image_path

def fetch_books():
    books = []
    books_folder = 'books'
    images_folder = os.path.join(books_folder, 'images')
    os.makedirs(images_folder, exist_ok=True)

    for book_file in os.listdir(books_folder):
        if book_file.endswith('.txt'):
            with open(os.path.join(books_folder, book_file), 'r', encoding='utf-8') as file:
                content = file.read()
                title = book_file.replace('.txt', '')
                books.append({'title': title, 'content': content, 'image': None, 'flipbook': None})
        elif book_file.endswith('.pdf'):
            pdf_path = os.path.join(books_folder, book_file)
            image_path = extract_first_page_as_image(pdf_path)
            flipbook_path = convert_pdf_to_flipbook(pdf_path)
            content, _ = extract_text_from_pdf(pdf_path)
            title = book_file.replace('.pdf', '')
            books.append({'title': title, 'content': content, 'image': image_path, 'flipbook': flipbook_path})

    with open('books.json', 'w', encoding='utf-8') as json_file:
        json.dump(books, json_file, ensure_ascii=False, indent=4)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")

    return text, []

if __name__ == '__main__':
    fetch_books()
