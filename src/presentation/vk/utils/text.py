import unicodedata


def normalize_for_comparison(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    
    text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    
    return text.strip()