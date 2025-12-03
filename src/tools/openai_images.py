"""OpenAI DALL-E 3 image generation tools."""

import os
import asyncio
import re
from typing import Literal, Optional, Dict, Set
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_binary_file
from utils.polish_support import POLISH_CHARS

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "dall-e-3")
OPENAI_DEFAULT_SIZE = os.getenv("OPENAI_IMAGE_SIZE", "1024x1024")
OPENAI_DEFAULT_QUALITY = os.getenv("OPENAI_IMAGE_QUALITY", "standard")

# Translation cache to avoid repeated API calls
_translation_cache: Dict[str, str] = {}

# Manual dictionary for common terms (faster than translation)
MANUAL_TRANSLATIONS: Dict[str, str] = {
    "Struktura": "Structure",
    "Elastyczny": "Flexible",
    "Elastyczna": "Flexible",
    "Odporny": "Resilient",
    "Odporna": "Resilient",
    "Prosty": "Simple",
    "Prosta": "Simple",
    "DOBRY KOD": "GOOD CODE",
    "ZASADY DOBREGO KODU": "PRINCIPLES OF GOOD CODE",
    "Powtarzalność": "Repetition",
    "Prostota": "Simplicity",
    "Projektowanie": "Design",
    "Empatia kodu": "Code Empathy",
    "kod": "code",
    "Kod": "Code",
    "KOD": "CODE",
}


def _detect_polish_words(text: str) -> Set[str]:
    """
    Detect Polish words in text by finding words containing Polish diacritics.
    
    Args:
        text: Text to analyze
        
    Returns:
        Set of detected Polish words
    """
    polish_words = set()
    
    # Polish diacritics pattern
    polish_chars_pattern = r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]'
    
    # Find all words (sequences of letters, including Polish characters)
    words = re.findall(r'\b\w+\b', text)
    
    for word in words:
        # Check if word contains Polish characters
        if re.search(polish_chars_pattern, word):
            # Filter out very short words and common English words that might have similar chars
            if len(word) > 2 and word.lower() not in ['i', 'a', 'o', 'u']:
                polish_words.add(word)
    
    return polish_words


def _translate_polish_word(word: str) -> str:
    """
    Translate a Polish word to English.
    Uses manual dictionary first, then falls back to automatic translation.
    
    Args:
        word: Polish word to translate
        
    Returns:
        English translation
    """
    # Check manual dictionary first (fastest)
    if word in MANUAL_TRANSLATIONS:
        return MANUAL_TRANSLATIONS[word]
    
    # Check cache
    if word in _translation_cache:
        return _translation_cache[word]
    
    # Try automatic translation
    try:
        from deep_translator import GoogleTranslator
        
        # Translate from Polish to English
        translator = GoogleTranslator(source='pl', target='en')
        translation = translator.translate(word)
        
        # Cache the translation
        _translation_cache[word] = translation
        
        return translation
    except Exception as e:
        # If translation fails, return original word
        # This prevents errors from breaking the image generation
        print(f"Warning: Could not translate '{word}': {e}")
        return word


def _enhance_prompt_for_text_rendering(prompt: str) -> str:
    """
    Enhance prompt to ensure English text rendering in DALL-E 3 images.
    Automatically detects Polish words and translates them to English.
    
    DALL-E 3 has limited support for non-English text, especially with diacritics.
    This function:
    1. Detects Polish words in the prompt
    2. Translates them to English (using cache and manual dictionary)
    3. Replaces Polish words with English translations
    4. Adds explicit instruction for English text rendering
    
    Args:
        prompt: Original prompt (may contain Polish text)
        
    Returns:
        Enhanced prompt with English text for rendering
    """
    # Detect Polish words
    polish_words = _detect_polish_words(prompt)
    
    # Start with original prompt
    enhanced = prompt
    
    # Replace detected Polish words with English translations
    for polish_word in polish_words:
        english_word = _translate_polish_word(polish_word)
        if english_word != polish_word:
            # Replace word, preserving case and context
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(polish_word) + r'\b'
            enhanced = re.sub(pattern, english_word, enhanced, flags=re.IGNORECASE)
    
    # Also check manual translations for common terms (case-insensitive)
    for polish, english in MANUAL_TRANSLATIONS.items():
        # Replace with word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(polish) + r'\b'
        enhanced = re.sub(pattern, english, enhanced, flags=re.IGNORECASE)
    
    # Add explicit instruction for text rendering
    text_instruction = (
        "\n\nIMPORTANT TEXT RENDERING INSTRUCTIONS: "
        "All visible text labels, titles, and words in the image must be written in English. "
        "Polish text in this prompt describes the content and layout, but any text that appears "
        "visually in the generated image should be in English for accurate rendering."
    )
    
    return enhanced + text_instruction


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
        
        # Enhance prompt for better text rendering (auto-translate Polish to English)
        enhanced_prompt = _enhance_prompt_for_text_rendering(prompt)
        
        # Generate image
        try:
            response = await client.images.generate(
                model=OPENAI_MODEL,
                prompt=enhanced_prompt,
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

