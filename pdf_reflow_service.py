import fitz  # pymupdf
from typing import Dict, Any, List
import io

def reflow_pdf_to_html(pdf_bytes: bytes) -> str:
    """
    converts a pdf file into a semantic, reflowable html document
    enables dyslexia tweaks (font, color, sizing) on previously locked documents
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        html_content = []
        
        for page_num, page in enumerate(doc):
            # Extract blocks (images, text)
            blocks = page.get_text("dict")["blocks"]
            
            page_html = f"<section class='pdf-page' id='page-{page_num+1}'>"
            
            for block in blocks:
                if block["type"] == 0: # Text Block
                    for line in block["lines"]:
                        line_text = ""
                        for span in line["spans"]:
                            text = span["text"]
                            font_size = span["size"]
                            flags = span["flags"] # bold/italic info
                            
                            # Semantic Heuristic: Detect Headings by Size
                            # If text is large (>15pt), treat as Heading
                            tag = "span"
                            if font_size > 18: tag = "h2"
                            elif font_size > 14: tag = "h3"
                            
                            # Filter styles: Ignore italics (flags & 2), keep bold (flags & 16)
                            style = ""
                            if flags & 16: style = "font-weight:bold;"
                            
                            line_text += f"<{tag} style='{style}'>{text}</{tag}> "
                        
                        # Wrap line in paragraph
                        page_html += f"<p>{line_text}</p>"
                        
                elif block["type"] == 1: # Image Block
                    # For accessibility, we should ideally caption images
                    # Here we put a placeholder or base64 encode the image (omitted for brevity)
                    page_html += "<div class='img-placeholder'>[Image Content]</div>"
            
            page_html += "</section><hr class='page-break'>"
            html_content.append(page_html)

        # Wrap in the same Dyslexia-Friendly Shell as web pages
        # Reusing the CSS from readability_service logic
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                :root {{ --bg-color: #E8F4F8; /* Light Blue tint default for PDFs */ }}
                body {{ 
                    background-color: var(--bg-color); 
                    font-family: 'Verdana', sans-serif; 
                    padding: 20px;
                    max-width: 800px;
                    margin: auto;
                }}
                p {{ margin-bottom: 15px; line-height: 1.6; }}
                h2, h3 {{ color: #2c3e50; margin-top: 30px; }}
                .page-break {{ border: 0; border-top: 1px dashed #ccc; margin: 50px 0; }}
            </style>
        </head>
        <body>
            {''.join(html_content)}
        </body>
        </html>
        """
        
        return full_html

    except Exception as e:
        return f"<h1>Error processing PDF</h1><p>{str(e)}</p>"
