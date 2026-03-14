from __future__ import annotations

from pathlib import Path
import json
import sys
import click

from .core import analyze_file, iter_files, SUPPORTED
from .utils import flatten


def format_text(record: dict) -> str:
    lines = [f"=== {record['path']} ==="]
    flat = flatten("", record)
    for key in sorted(flat.keys()):
        lines.append(f"{key}: {flat[key]}")
    return "\n".join(lines)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("target", type=click.Path(exists=True, path_type=Path))
@click.option("--recursive", "-r", is_flag=True, help="Scan directories recursively.")
@click.option("--json", "as_json", is_flag=True, help="Emit JSON output.")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Write output to file.")
@click.option("--hashes", is_flag=True, help="Calculate SHA256 and MD5 hashes.")
@click.option(
    "--ext",
    help="Comma-separated extension filter, e.g. .jpg,.pdf,.docx",
)
@click.option(
    "--all-files",
    is_flag=True,
    help="Scan all files, not just supported formats.",
)
def main(target: Path, recursive: bool, as_json: bool, output: Path | None, hashes: bool, ext: str | None, all_files: bool) -> None:
    """Analyze metadata for a file or directory."""
    exts = None
    if ext:
        exts = {e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower() for e in ext.split(",") if e.strip()}
    elif not all_files:
        exts = set(SUPPORTED)

    records = []
    errors = []

    for path in iter_files(target, recursive=recursive, exts=exts):
        try:
            records.append(analyze_file(path, include_hashes=hashes))
        except Exception as exc:
            errors.append({"path": str(path), "error": str(exc)})

    if as_json:
        payload = {"records": records, "errors": errors}
        content = json.dumps(payload, indent=2, default=str)
    else:
        blocks = [format_text(r) for r in records]
        if errors:
            blocks.append("=== errors ===")
            for err in errors:
                blocks.append(f"{err['path']}: {err['error']}")
        content = "\n\n".join(blocks)

    if output:
        output.write_text(content, encoding="utf-8")
    else:
        click.echo(content)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
