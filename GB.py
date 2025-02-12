import os
import json
import fitz  # PyMuPDF
from PIL import Image
import subprocess

def convert_pdf_to_flipbook(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    subprocess.run(['pdf2htmlEX', '--zoom', '1.3', '--dest-dir', output_folder, pdf_path])

def extract_first_page_as_image(pdf_path):
    doc = fitz.open(pdf_path)
    first_page = doc.load_page(0)  # Load the first page
    pix = first_page.get_pixmap()
    image_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page1.png"
    image_path = os.path.join('books', 'images', image_name)
    
    # Save the image
    pix.save(image_path)
    
    return image_path

def generate_index_html(book_folder, pages):
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipbook</title>
    <link rel="stylesheet" href="../../turnjs/turn.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }
        .flipbook {
            width: 800px;
            height: 400px;
            margin: 0 auto;
        }
        .flipbook .page {
            width: 400px;
            height: 400px;
        }
    </style>
</head>
<body>
    <div id="flipbook" class="flipbook">
    '''
    
    for page_content in pages:
        html_content += f'<div class="page">{page_content}</div>\n'

    html_content += '''
    </div>
    <script src="../../turnjs/turn.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            $('.flipbook').turn({
                width: 800,
                height: 400,
                autoCenter: true
            });
        });
    </script>
</body>
</html>
    '''

    with open(os.path.join(book_folder, 'index.html'), 'w', encoding='utf-8') as file:
        file.write(html_content)

def fetch_books():
    books_data = {}
    images_folder = os.path.join('books', 'images')
    os.makedirs(images_folder, exist_ok=True)

    for category in os.listdir('books'):
        category_path = os.path.join('books', category)
        if os.path.isdir(category_path) and category != 'images':
            books_data[category] = []
            for book_file in os.listdir(category_path):
                book_path = os.path.join(category_path, book_file)
                if book_file.endswith('.txt'):
                    with open(book_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        title = book_file.replace('.txt', '')
                        book_folder = os.path.join(category_path, title)
                        os.makedirs(book_folder, exist_ok=True)
                        pages = content.split('\n\n')  # Assuming each page is separated by a double newline
                        generate_index_html(book_folder, pages)
                        books_data[category].append({'title': title, 'content': content, 'image': None, 'flipbook': book_folder})
                elif book_file.endswith('.pdf'):
                    pdf_path = book_path
                    title = book_file.replace('.pdf', '')
                    book_folder = os.path.join(category_path, title)
                    os.makedirs(book_folder, exist_ok=True)
                    image_path = extract_first_page_as_image(pdf_path)
                    convert_pdf_to_flipbook(pdf_path, book_folder)
                    books_data[category].append({'title': title, 'content': "", 'image': image_path, 'flipbook': book_folder})

    with open('books.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_data, json_file, ensure_ascii=False, indent=4)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")

    return text, []

if __name__ == '__main__':
    fetch_books()
