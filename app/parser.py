import fitz  
import re

def parse_brand_kit(pdf_path):
    doc = fitz.open(pdf_path)
    text = " ".join([page.get_text() for page in doc])

    # chanck text into pages by information
    safepage = [page.get_text() for page in doc if 'Safe Zone' in page.get_text()]
    primpage = [page.get_text() for page in doc if 'Primary colors' in page.get_text()]
    fontpage = [page.get_text() for page in doc if 'Typography' in page.get_text() and 'Primary' in page.get_text()]
    
    # fonts
    primary_match = re.findall(r'Primary\n([^\n]+)', fontpage[0])
    secondary_match = re.findall(r'Secondary\n([^\n]+)', fontpage[0])
    fonts = [primary_match[0], secondary_match[0]]
    

    # colors in hex codes
    hex_codes = re.findall(r"#[A-Fa-f0-9]{6}", primpage[0])
    all_hex_codes = re.findall(r"(?:#|^)[A-Fa-f0-9]{6}", text)
    primary_colors = list(set(hex_codes))
    color_palette = list(set(all_hex_codes))

    # safe zone
    match = re.findall(r"([1-9][0-9]?px)", safepage[0])
    safe_zone = match[0] 
    
    return {
        "fonts": fonts,
        "safe_zone": safe_zone,
        "primary_colors": primary_colors,
        "color_palette": color_palette
    }