"""OpenAI DALL-E 3 image generation tools."""

import os
import asyncio
from typing import Literal, Optional
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_binary_file

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "dall-e-3")
OPENAI_DEFAULT_SIZE = os.getenv("OPENAI_IMAGE_SIZE", "1024x1024")
OPENAI_DEFAULT_QUALITY = os.getenv("OPENAI_IMAGE_QUALITY", "standard")


def _check_openai_available() -> tuple[bool, Optional[str]]:
    """
    Check if OpenAI API is available.
    
    Returns:
        Tuple of (is_available, error_message)
    """
    if not OPENAI_API_KEY:
        return False, "OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
    
    try:
        from openai import AsyncOpenAI
        return True, None
    except ImportError:
        return False, "OpenAI library not installed. Install with: pip install openai>=1.3.0"


async def generate_image_openai(
    prompt: str,
    output_path: str,
    size: Literal["1024x1024", "1024x1792", "1792x1024"] = "1024x1024",
    quality: Literal["standard", "hd"] = "standard"
) -> str:
    """
    Generate image using OpenAI DALL-E 3.
    
    Args:
        prompt: Image description prompt (supports Polish)
        output_path: Output file path
        size: Image size
        quality: Image quality (standard or hd)
        
    Returns:
        Success message or error message
    """
    # Check if OpenAI is available
    is_available, error_msg = _check_openai_available()
    if not is_available:
        return f"✗ Error: {error_msg}\n" \
               f"To use this feature:\n" \
               f"1. Install: pip install openai>=1.3.0\n" \
               f"2. Set OPENAI_API_KEY environment variable\n" \
               f"3. Get API key from: https://platform.openai.com/api-keys"
    
    try:
        from openai import AsyncOpenAI
        
        # Ensure output directory exists
        ensure_output_directory(output_path)
        abs_output = Path(output_path).absolute()
        
        # Initialize OpenAI client
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        # Generate image
        try:
            response = await client.images.generate(
                model=OPENAI_MODEL,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )
        except Exception as api_error:
            # Re-raise to be handled by outer exception handler
            raise api_error
        
        # Get image URL
        image_url = response.data[0].url
        
        # Download image
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as img_response:
                if img_response.status == 200:
                    image_data = await img_response.read()
                    write_binary_file(str(abs_output), image_data)
                    return f"✓ Image generated successfully: {abs_output}\n" \
                           f"   Prompt: {prompt[:100]}...\n" \
                           f"   Size: {size}, Quality: {quality}"
                else:
                    raise Exception(f"Failed to download image: HTTP {img_response.status}")
    
    except ImportError:
        return f"✗ Error: OpenAI library not installed.\n" \
               f"Install with: pip install openai>=1.3.0"
    except Exception as e:
        error_str = str(e).lower()
        
        # Check for insufficient quota / payment issues
        if "insufficient_quota" in error_str or "quota" in error_str or "payment" in error_str or "billing" in error_str:
            return f"✗ Error: Insufficient funds or quota exceeded on OpenAI account.\n" \
                   f"Your OpenAI account has no credits or quota has been exceeded.\n" \
                   f"To fix this:\n" \
                   f"1. Add payment method: https://platform.openai.com/account/billing\n" \
                   f"2. Add credits to your account\n" \
                   f"3. Check usage limits: https://platform.openai.com/usage\n" \
                   f"4. Wait for quota reset if you've hit rate limits\n\n" \
                   f"Original error: {str(e)}"
        
        # Check for invalid API key
        if "invalid" in error_str and "api" in error_str and "key" in error_str:
            return f"✗ Error: Invalid OpenAI API key.\n" \
                   f"Please check your OPENAI_API_KEY environment variable.\n" \
                   f"Get a new key: https://platform.openai.com/api-keys\n\n" \
                   f"Original error: {str(e)}"
        
        # Generic error
        return f"✗ Error generating image: {str(e)}\n" \
               f"Make sure OPENAI_API_KEY is set correctly and your account has sufficient credits."


async def generate_icon_openai(
    prompt: str,
    output_path: str,
    style: str = "flat design, minimalist, simple"
) -> str:
    """
    Generate icon using OpenAI DALL-E 3.
    Optimized for icon generation with specific style.
    
    Args:
        prompt: Icon description
        output_path: Output file path
        style: Additional style description
        
    Returns:
        Success message or error message
    """
    # Enhance prompt for icon generation
    enhanced_prompt = f"{prompt}, {style}, icon style, square format, transparent background"
    return await generate_image_openai(
        prompt=enhanced_prompt,
        output_path=output_path,
        size="1024x1024",
        quality="standard"
    )


async def generate_illustration_openai(
    prompt: str,
    output_path: str,
    style: str = "professional, technical illustration"
) -> str:
    """
    Generate illustration using OpenAI DALL-E 3.
    Optimized for concept illustrations.
    
    Args:
        prompt: Illustration description
        output_path: Output file path
        style: Additional style description
        
    Returns:
        Success message or error message
    """
    # Enhance prompt for illustration
    enhanced_prompt = f"{prompt}, {style}, high quality, detailed"
    return await generate_image_openai(
        prompt=enhanced_prompt,
        output_path=output_path,
        size="1024x1024",
        quality="hd"
    )

