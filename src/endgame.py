import fitz
import os
from typing import List, Optional, Dict, Any
import base64

current_dir = os.path.dirname(__file__)

# Go up one level to project root, then into "resources"
pdf_path = os.path.join(current_dir, "..", "resources", "100_Endgames.pdf")
toc_path = os.path.join(current_dir, "..", "resources", "TOC.txt")

pdf_path = os.path.abspath(pdf_path)
toc_path = os.path.abspath(toc_path)

class BookExtract:
    text_content: str
    image_blocks: List[Any]
    def __init__(self, text, images):
        self.text_content = text
        self.image_blocks = images
    def __str__(self) -> str:
        return f"BookExtract with {len(self.image_blocks)} pages and text length {len(self.text_content)} characters"

        

    

class BookUtilities:
    @staticmethod
    def get_table_of_contents() -> str:
        with open(toc_path,'r', encoding='utf-8') as f:
            toc = f.read()
        print('📜Retrieving the table of contents...')
        return toc
    @staticmethod
    def get_book_extract(start_page: int ,end_page: int) -> BookExtract:
        endgame_book = fitz.open(pdf_path)
        all_text = ''
        image_blocks =[]
        for i in range(start_page, end_page+1):
            page = endgame_book[i]
            # Get the text and append it to the global function variable
            current_text = page.get_text()
            all_text += f"PAGE:{i + 1}\n{current_text}\n\n"
            # Get the page image and append the it to the array
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes('png')
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            img_url = f"data:image/png;base64,{img_base64}"
            image_blocks.append({
                "type": "image_url",
                "image_url": {
                "url": img_url
                }
            })

        book = BookExtract(all_text,image_blocks)
        return book

