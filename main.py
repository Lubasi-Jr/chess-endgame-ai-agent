from src.endgame import BookUtilities
import json

extract = BookUtilities.get_book_extract(280,282)
print(extract.text_content)
