#!/usr/bin/env python3
"""
Script to convert JAK_DZIALA_SERWER_MCP.md to PDF with diagrams.
"""

import asyncio
import sys
import re
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tools.export import export_to_pdf
from utils.file_manager import read_file


def fix_image_paths(content: str, base_dir: Path) -> str:
    """Fix relative image paths to absolute paths."""
    # Pattern to match markdown images: ![alt](../output/image.png)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # If it's a relative path starting with ../
        if img_path.startswith('../'):
            # Convert to absolute path
            absolute_path = (base_dir.parent / img_path[3:]).absolute()
            return f'![{alt_text}]({absolute_path})'
        elif img_path.startswith('./'):
            absolute_path = (base_dir / img_path[2:]).absolute()
            return f'![{alt_text}]({absolute_path})'
        else:
            return match.group(0)
    
    return re.sub(pattern, replace_path, content)


async def main():
    """Convert markdown document to PDF."""
    base_dir = Path(__file__).parent.parent
    doc_path = base_dir / "docs" / "JAK_DZIALA_SERWER_MCP.md"
    output_path = "output/JAK_DZIALA_SERWER_MCP.pdf"
    
    print(f"Reading document: {doc_path}")
    markdown_content = read_file(str(doc_path))
    
    # Fix image paths to absolute paths
    # Use doc_path.parent (document's directory) instead of base_dir (project root)
    # because image paths like ../output/image.png are relative to the document location
    print("Fixing image paths...")
    markdown_content = fix_image_paths(markdown_content, doc_path.parent)
    
    print(f"Converting to PDF: {output_path}")
    result = await export_to_pdf(
        markdown_content=markdown_content,
        output_path=output_path,
        title="How the MCP Server Works - Step by Step Explanation",
        author="MCP Documentation Server",
        include_toc=True
    )
    
    print(result)
    
    if "✓" in result:
        print(f"\n✓ PDF generated successfully!")
        print(f"  Location: {Path(output_path).absolute()}")
    else:
        print(f"\n✗ Error generating PDF")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

