from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import mimetypes
from typing import Any


def iso_utc(ts: float | None) -> str | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def flatten(prefix: str, data: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in data.items():
        full = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            out.update(flatten(full, value))
        else:
            out[full] = value
    return out


def file_hashes(path: Path, chunk_size: int = 1024 * 1024) -> dict[str, str]:
    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            sha256.update(chunk)
            md5.update(chunk)
    return {"sha256": sha256.hexdigest(), "md5": md5.hexdigest()}


def guess_mime(path: Path) -> str | None:
    mime, _ = mimetypes.guess_type(str(path))
    return mime
