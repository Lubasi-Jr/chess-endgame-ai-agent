from fpdf import FPDF
import os



def save_text_as_txt(text: str, filename: str):
    """
    Saves a text string to a .txt file inside the 'lessons' folder.

    Args:
        text (str): The content to save.
        filename (str): Name of the file to be saved (without .txt extension).
    """
    print('Saved text as txt')


def save_text_as_pdf(content: str, filename: str):
    """
    Converts a large formatted text string into a PDF file.
    
    Args:
        text (str): The full essay or text content.
        filename (str): Name of the PDF file to be saved (without .pdf extension).
        margin_horizontal (int): Left and right margin in mm.
        margin_vertical (int): Top and bottom margin in mm.
    """
    # Set up the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Set up the path
    current_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(current_dir, "..", "lessons")
    pdf_path = os.path.abspath(pdf_path)
    os.makedirs(pdf_path, exist_ok=True)
    # Write content into the pdf
    pdf.multi_cell(0, 10, content)


    output_path = os.path.join(pdf_path, filename)
    pdf.output(output_path)

    if os.path.exists(output_path):
        print(f"💾 PDF saved as {filename}")
    else:
        print("File has not been saved")
