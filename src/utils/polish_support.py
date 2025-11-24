"""Polish language support utilities."""

import re
from typing import Dict


# Polish diacritics mapping
POLISH_CHARS = {
    'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
    'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
    'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
    'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
}


def normalize_polish_filename(filename: str) -> str:
    """
    Normalize Polish filename by replacing diacritics with ASCII equivalents.
    
    Args:
        filename: Original filename with Polish characters
        
    Returns:
        Normalized filename safe for filesystem
    """
    for polish_char, ascii_char in POLISH_CHARS.items():
        filename = filename.replace(polish_char, ascii_char)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove any other non-ASCII characters
    filename = re.sub(r'[^\w\-.]', '', filename)
    
    return filename


def get_pandoc_polish_options() -> Dict[str, str]:
    """
    Get Pandoc options for Polish language support.
    
    Returns:
        Dictionary of Pandoc options
    """
    return {
        "lang": "pl-PL",
        "pdf-engine": "xelatex",
        "mainfont": "DejaVu Sans",
        "monofont": "DejaVu Sans Mono",
        "variable": [
            "geometry:margin=2cm",
            "papersize:a4",
            "fontsize:11pt",
        ]
    }


def add_polish_metadata(metadata: Dict[str, str]) -> Dict[str, str]:
    """
    Add Polish language metadata to document.
    
    Args:
        metadata: Existing metadata dictionary
        
    Returns:
        Metadata with Polish language settings
    """
    metadata_with_polish = metadata.copy()
    metadata_with_polish.update({
        "lang": "pl-PL",
        "language": "polish",
    })
    return metadata_with_polish


def format_polish_date(date_format: str = "%d.%m.%Y") -> str:
    """
    Format current date in Polish format.
    
    Args:
        date_format: Date format string
        
    Returns:
        Formatted date string
    """
    from datetime import datetime
    return datetime.now().strftime(date_format)


# Polish month names
POLISH_MONTHS = {
    1: "stycznia", 2: "lutego", 3: "marca", 4: "kwietnia",
    5: "maja", 6: "czerwca", 7: "lipca", 8: "sierpnia",
    9: "września", 10: "października", 11: "listopada", 12: "grudnia"
}


def format_polish_date_full() -> str:
    """
    Format current date with Polish month names.
    
    Returns:
        Date string like "23 listopada 2025"
    """
    from datetime import datetime
    now = datetime.now()
    return f"{now.day} {POLISH_MONTHS[now.month]} {now.year}"

