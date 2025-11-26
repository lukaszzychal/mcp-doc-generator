#!/usr/bin/env python3
"""
Alternative script to convert JAK_DZIALA_SERWER_MCP.md to PDF using HTML intermediate.
Uses pandoc to HTML, then tries to convert HTML to PDF using available tools.
"""

import asyncio
import sys
import re
import subprocess
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.file_manager import read_file


def fix_image_paths(content: str, base_dir: Path) -> str:
    """Fix relative image paths to absolute paths."""
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        if img_path.startswith('../'):
            absolute_path = (base_dir.parent / img_path[3:]).absolute()
            return f'![{alt_text}]({absolute_path})'
        elif img_path.startswith('./'):
            absolute_path = (base_dir / img_path[2:]).absolute()
            return f'![{alt_text}]({absolute_path})'
        else:
            return match.group(0)
    
    return re.sub(pattern, replace_path, content)


async def convert_html_to_pdf(html_path: Path, pdf_path: Path) -> bool:
    """Try to convert HTML to PDF using available tools."""
    # Try Chrome/Chromium headless
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        shutil.which("chrome"),
        shutil.which("chromium"),
    ]
    
    chrome = None
    for path in chrome_paths:
        if path and Path(path).exists():
            chrome = path
            break
    
    if chrome:
        print(f"Using Chrome/Chromium: {chrome}")
        cmd = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--print-to-pdf=" + str(pdf_path.absolute()),
            "file://" + str(html_path.absolute()),
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            return result.returncode == 0
        except Exception as e:
            print(f"Chrome conversion failed: {e}")
    
    # Try wkhtmltopdf
    wkhtmltopdf = shutil.which("wkhtmltopdf")
    if wkhtmltopdf:
        print(f"Using wkhtmltopdf: {wkhtmltopdf}")
        cmd = [wkhtmltopdf, str(html_path), str(pdf_path)]
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            return result.returncode == 0
        except Exception as e:
            print(f"wkhtmltopdf conversion failed: {e}")
    
    return False


async def main():
    """Convert markdown document to PDF via HTML."""
    base_dir = Path(__file__).parent.parent
    doc_path = base_dir / "docs" / "JAK_DZIALA_SERWER_MCP.md"
    html_path = base_dir / "output" / "JAK_DZIALA_SERWER_MCP.html"
    pdf_path = base_dir / "output" / "JAK_DZIALA_SERWER_MCP.pdf"
    
    print(f"Reading document: {doc_path}")
    markdown_content = read_file(str(doc_path))
    
    # Fix image paths
    print("Fixing image paths...")
    markdown_content = fix_image_paths(markdown_content, base_dir)
    
    # Convert to HTML using pandoc
    print(f"Converting to HTML: {html_path}")
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
        tmp.write(markdown_content)
        tmp_path = tmp.name
    
    try:
        cmd = [
            "pandoc",
            tmp_path,
            "-o", str(html_path),
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--css=https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css",
            "-V", "title=How the MCP Server Works",
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"✗ Pandoc error: {result.stderr}")
            sys.exit(1)
        
        print("✓ HTML generated successfully")
        
        # Try to convert HTML to PDF
        print(f"Converting HTML to PDF: {pdf_path}")
        if await convert_html_to_pdf(html_path, pdf_path):
            print(f"✓ PDF generated successfully!")
            print(f"  Location: {pdf_path.absolute()}")
        else:
            print(f"\n⚠ Could not convert HTML to PDF automatically.")
            print(f"  HTML file saved at: {html_path.absolute()}")
            print(f"  You can:")
            print(f"    1. Open {html_path} in a browser and print to PDF")
            print(f"    2. Install xelatex: brew install --cask mactex (macOS)")
            print(f"    3. Use online converter")
    
    finally:
        import os
        os.unlink(tmp_path)


if __name__ == "__main__":
    asyncio.run(main())

