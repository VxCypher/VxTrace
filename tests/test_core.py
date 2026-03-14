from pathlib import Path
from vxtrace.core import classify, analyze_file


def test_classify_image():
    assert classify(Path("sample.jpg")) == "image"


def test_classify_pdf():
    assert classify(Path("sample.pdf")) == "pdf"
