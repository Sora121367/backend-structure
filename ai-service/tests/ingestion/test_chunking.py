import pytest

from app.ingestion.chunking import chunk_document
from app.ingestion.parsing import Anchor, Block, ParsedDocument


def doc(*blocks: Block, source_type="txt") -> ParsedDocument:
    return ParsedDocument(source_type=source_type, blocks=blocks)


def para(text: str, **anchor) -> Block:
    return Block(kind="paragraph", text=text, anchor=Anchor(**anchor))


def test_packs_small_blocks_into_one_chunk():
    chunks = chunk_document(doc(para("One.", paragraph_index=0), para("Two.", paragraph_index=1)))
    assert [c.text for c in chunks] == ["One.\n\nTwo."]
    assert chunks[0].anchor.paragraph_index == 0
    assert chunks[0].index == 0
    assert chunks[0].source_type == "txt"


def test_never_crosses_a_page():
    chunks = chunk_document(doc(para("A", page=1), para("B", page=2), source_type="pdf"))
    assert [(c.text, c.anchor.page) for c in chunks] == [("A", 1), ("B", 2)]
    assert [c.index for c in chunks] == [0, 1]


def test_never_crosses_a_slide():
    chunks = chunk_document(doc(para("A", slide=1), para("B", slide=2), source_type="pptx"))
    assert [c.anchor.slide for c in chunks] == [1, 2]


def test_never_crosses_a_section():
    blocks = [
        Block(
            kind="heading", text="Intro", heading_level=1, anchor=Anchor(section_path=("Intro",))
        ),
        para("Body", section_path=("Intro",)),
        Block(kind="heading", text="Next", heading_level=1, anchor=Anchor(section_path=("Next",))),
        para("More", section_path=("Next",)),
    ]
    chunks = chunk_document(doc(*blocks, source_type="docx"))
    assert [c.text for c in chunks] == ["Intro\n\nBody", "Next\n\nMore"]
    assert chunks[1].anchor.section_path == ("Next",)


def test_starts_a_new_chunk_when_full():
    chunks = chunk_document(doc(para("a" * 60), para("b" * 60)), max_chars=100)
    assert [c.text for c in chunks] == ["a" * 60, "b" * 60]


def test_splits_a_long_block_at_sentence_ends():
    text = "First sentence here. Second sentence here. Third sentence here."
    chunks = chunk_document(doc(para(text, page=3)), max_chars=45)
    assert [c.text for c in chunks] == [
        "First sentence here. Second sentence here.",
        "Third sentence here.",
    ]
    assert {c.anchor.page for c in chunks} == {3}


def test_splits_on_khmer_full_stop():
    text = "ប្រយោគទីមួយ។ ប្រយោគទីពីរ។"
    chunks = chunk_document(doc(para(text)), max_chars=15)
    assert [c.text for c in chunks] == ["ប្រយោគទីមួយ។", "ប្រយោគទីពីរ។"]


def test_hard_splits_text_without_sentence_ends():
    chunks = chunk_document(doc(para("word " * 10)), max_chars=12)
    assert all(len(c.text) <= 12 for c in chunks)
    assert " ".join(c.text for c in chunks).split() == ["word"] * 10


def test_hard_splits_a_single_unbroken_token():
    chunks = chunk_document(doc(para("x" * 25)), max_chars=10)
    assert [len(c.text) for c in chunks] == [10, 10, 5]


def test_every_chunk_fits_the_limit():
    text = " ".join(f"Sentence number {i}." for i in range(200))
    chunks = chunk_document(doc(para(text), para("tail")), max_chars=100)
    assert all(len(c.text) <= 100 for c in chunks)


def test_keeps_table_lines_together_when_they_fit():
    block = Block(kind="table", text="a | b\nc | d", anchor=Anchor())
    assert [c.text for c in chunk_document(doc(block))] == ["a | b\nc | d"]


def test_empty_document_gives_no_chunks():
    assert chunk_document(doc()) == []


def test_rejects_non_positive_limit():
    with pytest.raises(ValueError):
        chunk_document(doc(para("x")), max_chars=0)
