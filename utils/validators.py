# utils/validators.py
class TextValidator:
    @staticmethod
    def validate_input(text: str) -> bool:
        """Validate input text"""
        if not isinstance(text, str):
            return False
            
        text_length = len(text.strip())
        return 50 <= text_length <= 50000  # Adjust limits as needed
