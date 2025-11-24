"""Document export tools (PDF, DOCX) using Pandoc."""

import asyncio
import tempfile
import os
from typing import Optional
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_file, read_file
from utils.polish_support import get_pandoc_polish_options, format_polish_date_full


async def export_to_pdf(
    markdown_content: str,
    output_path: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    include_toc: bool = True
) -> str:
    """
    Convert Markdown to PDF using Pandoc with Polish language support.
    
    Args:
        markdown_content: Markdown content to convert
        output_path: Output PDF file path
        title: Document title
        author: Document author
        include_toc: Include table of contents
        
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
                "--pdf-engine=xelatex",
                "-V", "mainfont=DejaVu Sans",
                "-V", "monofont=DejaVu Sans Mono",
                "-V", "geometry:margin=2cm",
                "-V", "papersize=a4",
                "-V", "fontsize=11pt",
            ]
            
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
            
            return f"✓ PDF document generated successfully: {abs_output}"
        
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

