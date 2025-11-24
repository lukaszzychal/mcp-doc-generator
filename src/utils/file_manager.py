"""File management utilities."""

import os
from pathlib import Path
from typing import Optional


def ensure_output_directory(filepath: str) -> Path:
    """
    Ensure the output directory exists for the given filepath.
    
    Args:
        filepath: Path to the output file
        
    Returns:
        Path object for the file
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_absolute_path(filepath: str, base_dir: Optional[str] = None) -> str:
    """
    Get absolute path for a file.
    
    Args:
        filepath: Relative or absolute file path
        base_dir: Base directory for relative paths (default: current directory)
        
    Returns:
        Absolute file path as string
    """
    path = Path(filepath)
    if path.is_absolute():
        return str(path)
    
    if base_dir:
        return str(Path(base_dir) / path)
    
    return str(Path.cwd() / path)


def read_file(filepath: str, encoding: str = "utf-8") -> str:
    """
    Read file contents with proper encoding.
    
    Args:
        filepath: Path to the file
        encoding: File encoding (default: utf-8)
        
    Returns:
        File contents as string
    """
    with open(filepath, "r", encoding=encoding) as f:
        return f.read()


def write_file(filepath: str, content: str, encoding: str = "utf-8") -> None:
    """
    Write content to file with proper encoding.
    
    Args:
        filepath: Path to the file
        content: Content to write
        encoding: File encoding (default: utf-8)
    """
    path = ensure_output_directory(filepath)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def write_binary_file(filepath: str, content: bytes) -> None:
    """
    Write binary content to file.
    
    Args:
        filepath: Path to the file
        content: Binary content to write
    """
    path = ensure_output_directory(filepath)
    with open(path, "wb") as f:
        f.write(content)

