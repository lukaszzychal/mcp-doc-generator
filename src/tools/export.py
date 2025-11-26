"""Document export tools (PDF, DOCX) using Pandoc."""

import asyncio
import tempfile
import os
import re
from typing import Optional
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_file, read_file
from utils.polish_support import get_pandoc_polish_options, format_polish_date_full


def fix_image_paths(content: str, base_dir: Path) -> str:
    """
    Fix relative image paths to absolute paths for Pandoc.
    
    Args:
        content: Markdown content with image references
        base_dir: Base directory for resolving relative paths
        
    Returns:
        Markdown content with fixed image paths
    """
    # Pattern to match markdown images: ![alt](../output/image.png) or ![alt](./path/image.png)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_path(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # Skip if already absolute or URL
        if img_path.startswith('http://') or img_path.startswith('https://') or img_path.startswith('/'):
            return match.group(0)
        
        # Special handling for output/ paths - they should point to /app/output
        if img_path.startswith('output/'):
            absolute_path = Path('/app') / img_path
            return f'![{alt_text}]({absolute_path})'
        
        # Special handling for ../output/ paths - they should also point to /app/output
        if img_path.startswith('../output/'):
            absolute_path = Path('/app') / 'output' / img_path[10:]  # Remove '../output/'
            return f'![{alt_text}]({absolute_path})'
        
        # If it's a relative path starting with ../
        if img_path.startswith('../'):
            # Convert to absolute path relative to base_dir
            absolute_path = (base_dir.parent / img_path[3:]).absolute()
            return f'![{alt_text}]({absolute_path})'
        elif img_path.startswith('./'):
            # Convert to absolute path relative to base_dir
            absolute_path = (base_dir / img_path[2:]).absolute()
            return f'![{alt_text}]({absolute_path})'
        else:
            # Relative path without ./ or ../ - resolve relative to base_dir
            absolute_path = (base_dir / img_path).absolute()
            return f'![{alt_text}]({absolute_path})'
    
    return re.sub(pattern, replace_path, content)


async def export_to_pdf(
    markdown_content: Optional[str] = None,
    markdown_file_path: Optional[str] = None,
    output_path: str = "",
    title: Optional[str] = None,
    author: Optional[str] = None,
    include_toc: bool = True
) -> str:
    """
    Convert Markdown to PDF using Pandoc with Polish language support.
    Accepts either markdown content string or file path.
    
    Args:
        markdown_content: Markdown content to convert (optional if markdown_file_path is provided)
        markdown_file_path: Path to markdown file to convert (optional if markdown_content is provided)
        output_path: Output PDF file path
        title: Document title
        author: Document author
        include_toc: Include table of contents
        
    Returns:
        Success message
    """
    try:
        # Validate input
        if not markdown_content and not markdown_file_path:
            return "✗ Error: Either markdown_content or markdown_file_path must be provided"
        
        if not output_path:
            return "✗ Error: output_path is required"
        
        # Ensure output directory exists
        ensure_output_directory(output_path)
        
        # Get markdown content
        # If both are provided, prioritize markdown_content (user explicitly provided it)
        warning = ""
        if markdown_content and markdown_file_path:
            warning = f"⚠ Warning: Both markdown_content and markdown_file_path provided. Using markdown_content and ignoring markdown_file_path.\n"
        
        if markdown_content:
            # Use provided content - fix paths relative to /app (Docker container base)
            base_dir = Path("/app")
            markdown_content = fix_image_paths(markdown_content, base_dir)
        elif markdown_file_path:
            # Read from file
            file_path = Path(markdown_file_path)
            if not file_path.exists():
                return f"✗ Error: Markdown file not found: {markdown_file_path}"
            
            markdown_content = read_file(str(file_path))
            
            # Fix image paths relative to the markdown file's directory
            markdown_content = fix_image_paths(markdown_content, file_path.parent)
        
        # Prepare metadata
        metadata_yaml = "---\n"
        if title:
            metadata_yaml += f"title: \"{title}\"\n"
        if author:
            metadata_yaml += f"author: \"{author}\"\n"
        metadata_yaml += f"date: \"{format_polish_date_full()}\"\n"
        metadata_yaml += "lang: pl-PL\n"
        metadata_yaml += "---\n\n"
        
        full_content = metadata_yaml + markdown_content
        
        # Create temporary file for Markdown input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
            tmp.write(full_content)
            tmp_path = tmp.name
        
        try:
            abs_output = Path(output_path).absolute()
            
            # Try to detect available PDF engine
            import shutil
            pdf_engine = "xelatex"
            if not shutil.which("xelatex"):
                if shutil.which("pdflatex"):
                    pdf_engine = "pdflatex"
                elif shutil.which("wkhtmltopdf"):
                    pdf_engine = "wkhtmltopdf"
                else:
                    raise Exception("No PDF engine found. Install xelatex, pdflatex, or wkhtmltopdf")
            
            # Build Pandoc command
            cmd = [
                "pandoc",
                tmp_path,
                "-o", str(abs_output),
                f"--pdf-engine={pdf_engine}",
            ]
            
            # Add LaTeX-specific options only for LaTeX engines
            if pdf_engine in ["xelatex", "pdflatex"]:
                cmd.extend([
                    "-V", "mainfont=DejaVu Sans",
                    "-V", "monofont=DejaVu Sans Mono",
                    "-V", "geometry:margin=2cm",
                    "-V", "papersize=a4",
                    "-V", "fontsize=11pt",
                ])
            
            if include_toc:
                cmd.extend(["--toc", "--toc-depth=3"])
            
            # Run Pandoc
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
                raise Exception(f"Pandoc error: {error_msg}")
            
            success_msg = f"✓ PDF document generated successfully: {abs_output}"
            if warning:
                success_msg = warning + success_msg
            return success_msg
        
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
    
    except FileNotFoundError:
        return f"✗ Error: Pandoc not found.\n" \
               f"Install it with: brew install pandoc (macOS) or apt-get install pandoc texlive-xetex (Linux)"
    except Exception as e:
        return f"✗ Error generating PDF: {str(e)}"


async def export_to_docx(
    markdown_content: str,
    output_path: str,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> str:
    """
    Convert Markdown to DOCX using Pandoc with Polish language support.
    
    Args:
        markdown_content: Markdown content to convert
        output_path: Output DOCX file path
        title: Document title
        author: Document author
        
    Returns:
        Success message
    """
    try:
        # Ensure output directory exists
        ensure_output_directory(output_path)
        
        # Prepare metadata
        metadata_yaml = "---\n"
        if title:
            metadata_yaml += f"title: \"{title}\"\n"
        if author:
            metadata_yaml += f"author: \"{author}\"\n"
        metadata_yaml += f"date: \"{format_polish_date_full()}\"\n"
        metadata_yaml += "lang: pl-PL\n"
        metadata_yaml += "---\n\n"
        
        full_content = metadata_yaml + markdown_content
        
        # Create temporary file for Markdown input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp:
            tmp.write(full_content)
            tmp_path = tmp.name
        
        try:
            abs_output = Path(output_path).absolute()
            
            # Build Pandoc command
            cmd = [
                "pandoc",
                tmp_path,
                "-o", str(abs_output),
                "--toc",
                "--toc-depth=3"
            ]
            
            # Run Pandoc
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
                raise Exception(f"Pandoc error: {error_msg}")
            
            return f"✓ DOCX document generated successfully: {abs_output}"
        
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
    
    except FileNotFoundError:
        return f"✗ Error: Pandoc not found.\n" \
               f"Install it with: brew install pandoc (macOS) or apt-get install pandoc (Linux)"
    except Exception as e:
        return f"✗ Error generating DOCX: {str(e)}"


async def create_from_template(
    template_type: str,
    variables: dict,
    output_path: str
) -> str:
    """
    Generate document from template.
    
    Args:
        template_type: Type of template (adr, api_spec, c4_context, microservices_overview)
        variables: Variables to fill in the template
        output_path: Output file path
        
    Returns:
        Success message
    """
    try:
        # Get template path
        template_dir = Path(__file__).parent.parent / "templates"
        template_file = template_dir / f"{template_type}_template.md"
        
        if not template_file.exists():
            return f"✗ Error: Template '{template_type}' not found at {template_file}"
        
        # Read template
        template_content = read_file(str(template_file))
        
        # Replace variables
        content = template_content
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
        
        # Write output
        ensure_output_directory(output_path)
        write_file(output_path, content)
        
        abs_path = Path(output_path).absolute()
        return f"✓ Document created from template '{template_type}': {abs_path}"
    
    except Exception as e:
        return f"✗ Error creating document from template: {str(e)}"

