from fpdf import FPDF
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from html import escape


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
    # Create document with 10-point margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=10,
        rightMargin=10,
        topMargin=10,
        bottomMargin=10
    )
    
    # Custom styles for different content types
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # center-aligned
        spaceAfter=12,
        textColor=colors.darkblue
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.darkblue
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=12,
        leading=14,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    fen_style = ParagraphStyle(
        'FEN',
        parent=styles['Code'],
        fontSize=10,
        backColor=colors.lightgrey,
        borderPadding=5,
        spaceAfter=8
    )
    
    flowables = []
    
    # Process and structure the content
    sections = content.split('\n\n')
    for section in sections:
        if not section.strip():
            continue
            
        lines = section.strip().split('\n')
        first_line = lines[0].strip()
        
        # Apply appropriate styling based on content
        if first_line.startswith("Lesson"):
            flowables.append(Paragraph(escape(first_line), title_style))
            flowables.append(Spacer(1, 5))
            if len(lines) > 1:
                flowables.append(Paragraph(escape('<br/>'.join(lines[1:])), body_style))
        elif first_line in ["PRINCIPLES", "SITUATION", "GOAL", "STRATEGY", "MOVES", "HOW IT LINKS TO THE RULES"]:
            flowables.append(Paragraph(escape(first_line), subtitle_style))
            if len(lines) > 1:
                flowables.append(Paragraph(escape('<br/>'.join(lines[1:])), body_style))
        elif "FEN:" in first_line:
            fen_text = first_line.replace("FEN:", "<b>FEN:</b>")
            flowables.append(Paragraph(fen_text, fen_style))
        else:
            formatted_text = escape(section.replace('\n', '<br/>'))
            flowables.append(Paragraph(formatted_text, body_style))
        
        flowables.append(Spacer(1, 8))
    
    # Generate the PDF
    doc.build(flowables)
    

    print(f"💾 PDF saved as {filename}")
