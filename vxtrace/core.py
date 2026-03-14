from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable
import os

from .extractors import image_metadata, pdf_metadata, docx_metadata, xlsx_metadata
from .utils import file_hashes, guess_mime, iso_utc

SUPPORTED = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp", ".gif",
    ".pdf", ".docx", ".xlsx",
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp", ".gif"}


def classify(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext == ".pdf":
        return "pdf"
    if ext == ".docx":
        return "docx"
    if ext == ".xlsx":
        return "xlsx"
    return "generic"


def base_metadata(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": str(path.resolve()),
        "name": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "created": iso_utc(getattr(stat, "st_ctime", None)),
        "modified": iso_utc(getattr(stat, "st_mtime", None)),
        "accessed": iso_utc(getattr(stat, "st_atime", None)),
        "mime_type": guess_mime(path),
        "type": classify(path),
    }


def analyze_file(path: Path, include_hashes: bool = False) -> dict[str, Any]:
    path = path.expanduser().resolve()
    data = base_metadata(path)
    file_type = data["type"]

    if file_type == "image":
        data["image"] = image_metadata(path)
    elif file_type == "pdf":
        data.update(pdf_metadata(path))
    elif file_type == "docx":
        data.update(docx_metadata(path))
    elif file_type == "xlsx":
        data.update(xlsx_metadata(path))

    if include_hashes:
        data.update(file_hashes(path))
    return data


def iter_files(root: Path, recursive: bool = False, exts: set[str] | None = None) -> Iterable[Path]:
    root = root.expanduser().resolve()
    if root.is_file():
        if exts is None or root.suffix.lower() in exts:
            yield root
        return

    walk = root.rglob("*") if recursive else root.glob("*")
    for p in walk:
        if p.is_file():
            if exts is None or p.suffix.lower() in exts:
                yield p
