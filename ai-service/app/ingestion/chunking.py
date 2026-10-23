"""Split a ParsedDocument into chunks that each cite one place (spec Section 5, Chunking).

A chunk never crosses a page, slide or section, so its anchor is exact and a citation can point
at it. Size is counted in characters: the embedding model (and its tokenizer) is not chosen yet.
"""

import re
from collections.abc import Iterator

from pydantic import BaseModel, ConfigDict

from app.ingestion.parsing.models import Anchor, Block, ParsedDocument, SourceType

DEFAULT_MAX_CHARS = 1200
_SEPARATOR = "\n\n"
_SENTENCE_END = re.compile(r"(?<=[.!?។៕])\s+")  # includes the Khmer full stops


class Chunk(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    index: int  # position in the document, starting at 0
    text: str
    source_type: SourceType
    anchor: Anchor  # of the first block; page, slide and section_path hold for the whole chunk


def _hard_split(text: str, max_chars: int) -> Iterator[str]:
    """Last resort for text with no sentence ends: cut at spaces, or mid-word if there are none."""
    while len(text) > max_chars:
        cut = text.rfind(" ", 0, max_chars + 1)
        if cut <= 0:
            cut = max_chars
        yield text[:cut].strip()
        text = text[cut:].strip()
    if text:
        yield text


def _split_text(text: str, max_chars: int) -> Iterator[str]:
    """Pieces of at most max_chars, preferring to cut after a sentence, then at a line."""
    current = ""
    for sentence in text.split("\n"):
        for part in _SENTENCE_END.split(sentence):
            if len(part) > max_chars:
                if current:
                    yield current
                    current = ""
                yield from _hard_split(part, max_chars)
            elif current and len(current) + 1 + len(part) > max_chars:
                yield current
                current = part
            else:
                current = f"{current} {part}" if current else part
    if current:
        yield current


def _group_key(block: Block) -> tuple[int | None, int | None, tuple[str, ...]]:
    return block.anchor.page, block.anchor.slide, block.anchor.section_path


def chunk_document(document: ParsedDocument, max_chars: int = DEFAULT_MAX_CHARS) -> list[Chunk]:
    if max_chars < 1:
        raise ValueError("max_chars must be positive")

    chunks: list[Chunk] = []

    def emit(text: str, anchor: Anchor) -> None:
        chunks.append(
            Chunk(index=len(chunks), text=text, source_type=document.source_type, anchor=anchor)
        )

    pending: list[str] = []
    pending_anchor: Anchor | None = None

    def flush() -> None:
        nonlocal pending, pending_anchor
        if pending and pending_anchor is not None:
            emit(_SEPARATOR.join(pending), pending_anchor)
        pending, pending_anchor = [], None

    previous_key = None
    for block in document.blocks:
        key = _group_key(block)
        if key != previous_key:
            flush()
            previous_key = key
        pieces = (
            [block.text] if len(block.text) <= max_chars else _split_text(block.text, max_chars)
        )
        for piece in pieces:
            size = sum(len(t) for t in pending) + len(_SEPARATOR) * len(pending)
            if pending and size + len(piece) > max_chars:
                flush()
            if pending_anchor is None:
                pending_anchor = block.anchor
            pending.append(piece)
    flush()
    return chunks
