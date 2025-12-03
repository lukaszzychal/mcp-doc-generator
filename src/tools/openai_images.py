"""OpenAI DALL-E 3 image generation tools."""

import os
import asyncio
import re
import math
from typing import Literal, Optional, Dict, Set, List, Tuple, Any
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


def _enhance_prompt_for_no_text(prompt: str) -> str:
    """
    Enhance prompt to generate images WITHOUT any text labels.
    This is part of the hybrid approach: DALL-E 3 generates graphics,
    PIL adds text overlay for perfect text rendering.
    
    Args:
        prompt: Original prompt (may contain text descriptions)
        
    Returns:
        Enhanced prompt that explicitly excludes text from image
    """
    # Detect Polish words and translate for description (not for rendering)
    polish_words = _detect_polish_words(prompt)
    
    # Start with original prompt
    enhanced = prompt
    
    # Replace detected Polish words with English translations (for description clarity)
    for polish_word in polish_words:
        english_word = _translate_polish_word(polish_word)
        if english_word != polish_word:
            pattern = r'\b' + re.escape(polish_word) + r'\b'
            enhanced = re.sub(pattern, english_word, enhanced, flags=re.IGNORECASE)
    
    # Also check manual translations for common terms
    for polish, english in MANUAL_TRANSLATIONS.items():
        pattern = r'\b' + re.escape(polish) + r'\b'
        enhanced = re.sub(pattern, english, enhanced, flags=re.IGNORECASE)
    
    # Add explicit instruction to EXCLUDE text from image
    no_text_instruction = (
        "\n\nCRITICAL: DO NOT include any text, labels, titles, words, letters, or written content "
        "in the generated image. Only visual elements: shapes, icons, lines, colors, geometric patterns, "
        "illustrations, and graphics. All text will be added separately. Focus on creating beautiful "
        "visual design without any textual elements."
    )
    
    return enhanced + no_text_instruction


def _extract_text_labels(prompt: str) -> List[Dict[str, Any]]:
    """
    Extract text labels that should appear in the image from user prompt.
    
    Args:
        prompt: User prompt containing text labels
        
    Returns:
        List of text labels with metadata (text, position hint, type)
    """
    labels = []
    seen_texts = set()
    
    # Pattern 1: Central node text (common in mind maps) - check first
    central_patterns = [
        r'central[^.]*?["\']([^"\']+)["\']',
        r'central[^.]*?node[^.]*?["\']([^"\']+)["\']',
        r'center[^.]*?["\']([^"\']+)["\']',
        r'central[^.]*?=([^=]+?)(?:and|with|,|\n|$)',
    ]
    central_text = None
    for pattern in central_patterns:
        matches = re.findall(pattern, prompt, re.IGNORECASE)
        for match in matches:
            text = match.strip()
            # Only take longer central texts (avoid single words)
            if len(text) > 10 and text.upper() not in seen_texts:
                seen_texts.add(text.upper())
                central_text = text
                labels.append({
                    'text': text,
                    'type': 'central',
                    'position': 'center'
                })
                break
        if central_text:
            break
    
    # Add all words from central text to seen_texts to avoid duplicates
    if central_text:
        central_words = re.findall(r'\b\w+\b', central_text)
        for word in central_words:
            seen_texts.add(word.upper())
    
    # Pattern 2: Quoted text (e.g., "GOOD CODE", 'SOLID') - but not central
    quoted_pattern = r'["\']([^"\']+)["\']'
    quoted_matches = re.findall(quoted_pattern, prompt)
    for match in quoted_matches:
        text = match.strip()
        # Filter out very short matches and common words
        if (len(text) > 2 and 
            text.upper() not in ['THE', 'AND', 'OR', 'FOR'] and
            text.upper() not in seen_texts):
            # Check if this is part of central node (already added)
            is_central = any(text.upper() in label['text'].upper() for label in labels if label.get('type') == 'central')
            if not is_central:
                seen_texts.add(text.upper())
                labels.append({
                    'text': text,
                    'type': 'quoted',
                    'position': 'auto'
                })
    
    # Pattern 3: Uppercase acronyms (SOLID, DRY, KISS, GRASP, CUPID, etc.)
    acronym_pattern = r'\b([A-Z]{2,10})\b'
    acronym_matches = re.findall(acronym_pattern, prompt)
    for match in acronym_matches:
        # Common programming acronyms
        if (match in ['SOLID', 'DRY', 'KISS', 'GRASP', 'CUPID', 'SRP', 'OCP', 'LSP', 'ISP', 'DIP'] and
            match not in seen_texts):
            seen_texts.add(match)
            labels.append({
                'text': match,
                'type': 'acronym',
                'position': 'auto'
            })
    
    # Pattern 4: Text after colons (e.g., "Title: Good Code") - but skip if already found
    colon_pattern = r'[:]\s*([A-Z][^:\n]+?)(?:\n|$)'
    colon_matches = re.findall(colon_pattern, prompt)
    for match in colon_matches:
        text = match.strip()
        # Skip if contains multiple acronyms (already extracted separately)
        if (len(text) > 2 and len(text) < 100 and
            text.upper() not in seen_texts and
            not any(acronym in text for acronym in ['SOLID', 'DRY', 'KISS', 'GRASP', 'CUPID'])):
            seen_texts.add(text.upper())
            labels.append({
                'text': text,
                'type': 'labeled',
                'position': 'auto'
            })
    
    # Pattern 5: Text in parentheses with common keywords
    paren_pattern = r'\(([A-Z][^)]+)\)'
    paren_matches = re.findall(paren_pattern, prompt)
    for match in paren_matches:
        text = match.strip()
        if (any(keyword in text.upper() for keyword in ['CODE', 'DESIGN', 'STRUCTURE', 'PRINCIPLE']) and
            text.upper() not in seen_texts):
            seen_texts.add(text.upper())
            labels.append({
                'text': text,
                'type': 'parenthetical',
                'position': 'auto'
            })
    
    return labels


def _add_text_overlay(
    image_path: str,
    text_labels: List[Dict[str, Any]],
    output_path: str
) -> str:
    """
    Add text overlay to image using PIL/Pillow.
    
    Args:
        image_path: Path to base image (from DALL-E 3)
        text_labels: List of text labels to add
        output_path: Path to save final image
        
    Returns:
        Success message or error message
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Load image
        img = Image.open(image_path)
        img_width, img_height = img.size
        
        # Create drawing context
        draw = ImageDraw.Draw(img)
        
        # Try to load DejaVu Sans font (supports Polish characters)
        # Fallback to default font if not available
        try:
            # Common paths for DejaVu Sans in Docker
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
                '/System/Library/Fonts/Helvetica.ttc',  # macOS fallback
            ]
            font = None
            for path in font_paths:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, size=48)
                    break
            
            if font is None:
                # Use default font
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()
        
        # Calculate positions for labels
        num_labels = len(text_labels)
        
        # For mind maps: central label in center, branches around
        central_labels = [l for l in text_labels if l.get('position') == 'center' or l.get('type') == 'central']
        branch_labels = [l for l in text_labels if l not in central_labels]
        
        # Add central label(s)
        for label in central_labels:
            text = label['text']
            # Split long text into multiple lines
            words = text.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                word_length = len(word) * 10  # Approximate
                if current_length + word_length > 40 and current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length
                else:
                    current_line.append(word)
                    current_length += word_length + 1
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw text in center
            y_offset = img_height // 2 - (len(lines) * 30) // 2
            for i, line in enumerate(lines):
                # Get text size for centering
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (img_width - text_width) // 2
                y = y_offset + i * 35
                
                # Draw text with outline for readability
                # Draw outline (black)
                for adj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    draw.text((x + adj[0], y + adj[1]), line, font=font, fill='black')
                # Draw main text (white)
                draw.text((x, y), line, font=font, fill='white')
        
        # Add branch labels (positioned around center)
        if branch_labels:
            angle_step = 360 / len(branch_labels)
            radius = min(img_width, img_height) * 0.35
            
            for i, label in enumerate(branch_labels):
                text = label['text']
                angle = math.radians(i * angle_step)
                
                # Calculate position
                center_x = img_width // 2
                center_y = img_height // 2
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                
                # Get text size for centering
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x -= text_width // 2
                y -= text_height // 2
                
                # Draw text with outline
                for adj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    draw.text((x + adj[0], y + adj[1]), text, font=font, fill='black')
                draw.text((x, y), text, font=font, fill='white')
        
        # Save image
        img.save(output_path, 'PNG')
        return f"✓ Text overlay added successfully"
        
    except ImportError:
        return f"✗ Error: Pillow library not installed. Install with: pip install Pillow>=10.0.0"
    except Exception as e:
        return f"✗ Error adding text overlay: {str(e)}"


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
    quality: Literal["standard", "hd"] = "standard",
    add_text_overlay: bool = True
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
        
        # Extract text labels before modifying prompt (for hybrid approach)
        text_labels = []
        if add_text_overlay:
            text_labels = _extract_text_labels(prompt)
        
        # Enhance prompt: generate image WITHOUT text (hybrid approach)
        # Text will be added by PIL for perfect rendering
        enhanced_prompt = _enhance_prompt_for_no_text(prompt)
        
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
                    
                    # Save base image (without text) to temporary location
                    base_image_path = str(abs_output).replace('.png', '_base.png')
                    write_binary_file(base_image_path, image_data)
                    
                    # Add text overlay if requested and labels were found
                    if add_text_overlay and text_labels:
                        overlay_result = _add_text_overlay(base_image_path, text_labels, str(abs_output))
                        # Remove temporary base image
                        try:
                            os.remove(base_image_path)
                        except Exception:
                            pass
                        
                        if "Error" in overlay_result:
                            # If overlay fails, use base image
                            import shutil
                            shutil.copy(base_image_path, str(abs_output))
                            return f"✓ Image generated (text overlay failed): {abs_output}\n" \
                                   f"   {overlay_result}\n" \
                                   f"   Prompt: {prompt[:100]}...\n" \
                                   f"   Size: {size}, Quality: {quality}"
                        else:
                            return f"✓ Image generated with text overlay: {abs_output}\n" \
                                   f"   Labels added: {len(text_labels)}\n" \
                                   f"   Prompt: {prompt[:100]}...\n" \
                                   f"   Size: {size}, Quality: {quality}"
                    else:
                        # No text overlay requested or no labels found
                        if os.path.exists(base_image_path) and base_image_path != str(abs_output):
                            import shutil
                            shutil.move(base_image_path, str(abs_output))
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
    style: str = "professional, technical illustration",
    add_text_overlay: bool = True
) -> str:
    """
    Generate illustration using OpenAI DALL-E 3.
    Optimized for concept illustrations.
    Uses hybrid approach: DALL-E 3 generates graphics, PIL adds text overlay.
    
    Args:
        prompt: Illustration description
        output_path: Output file path
        style: Additional style description
        add_text_overlay: Whether to add text overlay using PIL (default: True)
        
    Returns:
        Success message or error message
    """
    # Enhance prompt for illustration
    enhanced_prompt = f"{prompt}, {style}, high quality, detailed"
    return await generate_image_openai(
        prompt=enhanced_prompt,
        output_path=output_path,
        size="1024x1024",
        quality="hd",
        add_text_overlay=add_text_overlay
    )

