import re
import unicodedata

_WHITESPACE = re.compile(r"\s+")


def normalize(text: str) -> str:
    """NFC (Khmer and accented Latin compare equal), single spaces, no control characters.

    Zero-width spaces are kept: Khmer uses them as word breaks.
    """
    text = _WHITESPACE.sub(" ", unicodedata.normalize("NFC", text))
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cc").strip()


def table_text(rows: list[list[str]]) -> str:
    """One line per row, cells joined by ' | '. Used for DOCX and PPTX tables."""
    return "\n".join(" | ".join(row) for row in rows if any(row))
