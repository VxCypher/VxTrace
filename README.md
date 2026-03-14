# VxTrace
<<<<<<< HEAD

Metadata investigation toolkit for researchers and analysts.

VxTrace extracts non-sensitive file metadata from common formats and can output either
human-readable text or JSON. It is built for local analysis and documentation workflows.

## Features

- Image metadata (JPEG, PNG, TIFF, WebP, HEIC/HEIF if supported by Pillow)
- PDF metadata
- DOCX core properties
- XLSX workbook properties
- File-system metadata (size, hashes, timestamps)
- Batch directory scanning
- JSON output for automation
- Simple CLI

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Usage

Analyze one file:

```bash
vxtrace sample.jpg
```

Analyze a directory recursively:

```bash
vxtrace ./evidence --recursive
```

Save JSON report:

```bash
vxtrace ./samples --recursive --json --output report.json
```

Calculate hashes:

```bash
vxtrace sample.pdf --hashes
```

Limit to certain file types:

```bash
vxtrace ./samples --recursive --ext .jpg,.pdf,.docx
```

## Examples

Text output:

```text
=== /path/to/file.jpg ===
type: image
size_bytes: 382921
mime_type: image/jpeg
sha256: ...
created: 2026-03-14T10:04:00
modified: 2026-03-14T10:04:02
image.width: 1024
image.height: 1024
exif.DateTimeOriginal: 2026:03:14 10:03:59
```

JSON output:

```json
[
  {
    "path": "/path/to/file.pdf",
    "type": "pdf",
    "size_bytes": 88212,
    "mime_type": "application/pdf",
    "pdf": {
      "Author": "Keith",
      "Producer": "LibreOffice"
    }
  }
]
```

## Safety / Scope

VxTrace is for defensive, local metadata inspection. It does not bypass encryption, recover deleted data, or perform covert collection.

## Roadmap

- CSV output
- EXIF removal option
- HTML report generation
- Better MIME detection fallback
- Unit tests for more file types

## License

MIT
=======
Metadata investigation toolkit
>>>>>>> 4a32863fa460a29acf47af9cccb8b3bb879f923c
