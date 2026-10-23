import codecs
import re
from pathlib import Path

from app.ingestion.parsing._text import normalize
from app.ingestion.parsing.errors import DocumentParseError
from app.ingestion.parsing.models import Anchor, Block, ParsedDocument

_PARAGRAPH_BREAK = re.compile(r"\n[ \t]*\n")


def _decode(data: bytes) -> str:
    if data.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return data.decode("utf-16")
    if b"\x00" in data:
        raise DocumentParseError("The file contains binary data, not text.")
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        pass
    try:
        return data.decode("cp1252")
    except UnicodeDecodeError as e:
        raise DocumentParseError("The text encoding is not supported; save it as UTF-8.") from e


def parse_txt(path: Path) -> ParsedDocument:
    text = _decode(path.read_bytes()).replace("\r\n", "\n").replace("\r", "\n")
    blocks: list[Block] = []
    for raw in _PARAGRAPH_BREAK.split(text):
        if paragraph := normalize(raw):
            anchor = Anchor(paragraph_index=len(blocks))
            blocks.append(Block(kind="paragraph", text=paragraph, anchor=anchor))
    if not blocks:
        raise DocumentParseError("The file has no text.")
    return ParsedDocument(source_type="txt", blocks=tuple(blocks))
