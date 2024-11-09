# utils/text_processor.py
import re
from typing import List

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        return text.strip()
    
    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """Split text into sentences"""
        return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    @staticmethod
    def extract_words(text: str) -> List[str]:
        """Extract words from text"""
        return [w.lower() for w in re.findall(r'\w+', text)]

# utils/validators.py
from typing import Tuple
from config import settings

class TextValidator:
    @staticmethod
    def validate_input(text: str) -> bool:
        """Validate input text"""
        if not isinstance(text, str):
            return False
            
        text_length = len(text.strip())
        return (text_length >= settings.MIN_TEXT_LENGTH and 
                text_length <= settings.MAX_TEXT_LENGTH)
    
    @staticmethod
    def validate_language(text: str) -> Tuple[bool, str]:
        """Validate text language"""
        try:
            from langdetect import detect
            lang = detect(text)
            return lang == 'en', lang
        except:
            return True, 'unknown'  # Default to accepting text if language detection fails