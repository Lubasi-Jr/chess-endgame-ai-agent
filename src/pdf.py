from fpdf import FPDF
import os


def save_text_as_txt(text: str, filename: str):
    """
    Saves a text string to a .txt file inside the 'lessons' folder.

    Args:
        text (str): The content to save.
        filename (str): Name of the file to be saved (without .txt extension).
    """
    # Determine the root directory and 'lessons' path
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lessons_path = os.path.join(root_dir, "lessons")
    os.makedirs(lessons_path, exist_ok=True)  # Ensure directory exists

    # Full output path
    output_file_path = os.path.join(lessons_path, f"{filename}.txt")

    # Write text to file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"💾 Text file saved as {filename}.txt")

    
def save_text_as_pdf(text: str, filename: str, margin_horizontal: int = 10, margin_vertical: int = 10):
    """
    Converts a large formatted text string into a PDF file.
    
    Args:
        text (str): The full essay or text content.
        filename (str): Name of the PDF file to be saved (without .pdf extension).
        margin_horizontal (int): Left and right margin in mm.
        margin_vertical (int): Top and bottom margin in mm.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=margin_vertical)
    pdf.add_page()

    # Set margins
    pdf.set_margins(left=margin_horizontal, top=margin_vertical, right=margin_horizontal)

    # Set font
    pdf.set_font("Arial", size=12)

    # Add the text
    pdf.multi_cell(0, 10, text)

    # Build full path: root -> lessons/filename.pdf
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lessons_path = os.path.join(root_dir, "lessons")
    os.makedirs(lessons_path, exist_ok=True)  # Ensure directory exists

    output_file_path = os.path.join(lessons_path, f"{filename}.pdf")
    pdf.output(output_file_path)

    print(f"💾 PDF saved as {filename}.pdf")
