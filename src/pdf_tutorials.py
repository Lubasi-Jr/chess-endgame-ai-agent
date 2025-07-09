from langchain.agents import create_react_agent
import fitz
import os

current_dir = os.path.dirname(__file__)

# Go up one level to project root, then into "resources"
pdf_path = os.path.join(current_dir, "..", "resources", "100_Endgames.pdf")
toc_path = os.path.join(current_dir, "..", "resources", "TOC.txt")

pdf_path = os.path.abspath(pdf_path)
toc_path = os.path.abspath(toc_path)


doc = fitz.open(pdf_path)

# Pages 5–7 are TOC pages (0-indexed: page 5 = page 6)
toc_start = 5
toc_end = 7
table_of_contents = ""

for page_num in range(toc_start, toc_end + 1):
    page = doc[page_num]
    links = page.get_links()


    table_of_contents += f"\n--- Page {page_num + 1} (TOC) ---\n"
    #print(f"\n--- Page {page_num + 1} (TOC) ---")

    for link in links:
        if link['kind'] == fitz.LINK_GOTO:
            dest_page = link['page'] + 1  # Convert from 0-based to 1-based
            rect = link['from']  # clickable rectangle
            text = page.get_textbox(rect).strip()
            table_of_contents += f"{text} ---> Page {dest_page}\n"
            #print(f"{text} ---> Page {dest_page}")

os.makedirs('resources', exist_ok=True)
with open(toc_path,'w',encoding='utf-8') as f:
    f.write(table_of_contents)
    print("✅ Table of Contents saved to resources/TOC.txt")

# You can use fitz to extract text from particular page. Remember that it is 0-indexed
page = doc[37]  # Page 38 is the page that talks about Imprisoning the stronger side's king
print("Page 38 is the page that talks about Imprisoning the stronger side's king")

text = page.get_text()
print(text)

