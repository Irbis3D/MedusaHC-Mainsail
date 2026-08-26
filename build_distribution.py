#!/usr/bin/env python3
"""Build a pinned MedusaHC Mainsail zip from an official Mainsail zip."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
METADATA = ROOT / "upstream.json"
SCRIPT = ROOT / "integration" / "mainsail-medusahc.js"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(source_zip: Path, output_zip: Path) -> dict[str, str]:
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="medusahc-mainsail-") as temporary:
        staging = Path(temporary) / "web"
        staging.mkdir()
        with zipfile.ZipFile(source_zip) as archive:
            staging_resolved = staging.resolve()
            for member in archive.infolist():
                resolved = (staging / member.filename).resolve()
                if staging_resolved not in resolved.parents and resolved != staging_resolved:
                    raise SystemExit("Mainsail archive contains an unsafe path")
            archive.extractall(staging)
        candidates = [staging] + [item for item in staging.iterdir() if item.is_dir()]
        web_root = next((item for item in candidates if (item / "index.html").is_file()), None)
        if web_root is None:
            raise SystemExit("Official Mainsail archive does not contain index.html")
        index = web_root / "index.html"
        text = index.read_text(encoding="utf-8")
        marker = '<script src="/mainsail-medusahc.js"></script>'
        if marker not in text:
            if "</body>" not in text:
                raise SystemExit("Mainsail index.html does not contain </body>")
            text = text.replace("</body>", f"    {marker}\n    </body>", 1)
            index.write_text(text, encoding="utf-8")
        shutil.copy2(SCRIPT, web_root / "mainsail-medusahc.js")
        release_info = {
            "project_name": "medusahc-mainsail",
            "project_owner": "Irbis3D",
            "version": (
                f"{metadata['upstream_version']}-medusahc."
                f"{metadata['integration_version']}"
            ),
            "mainsail_upstream": metadata["upstream_version"],
        }
        (web_root / "release_info.json").write_text(
            json.dumps(release_info, separators=(",", ":")), encoding="utf-8"
        )
        output_zip.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in sorted(web_root.rglob("*")):
                if item.is_file():
                    archive.write(item, item.relative_to(web_root).as_posix())
    result = {
        "output": str(output_zip),
        "sha256": sha256(output_zip),
        "upstream_sha256": sha256(source_zip),
        "upstream_version": metadata["upstream_version"],
        "integration_version": metadata["integration_version"],
    }
    output_zip.with_suffix(output_zip.suffix + ".build.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("output_zip", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.source_zip.resolve(), args.output_zip.resolve()), indent=2))


if __name__ == "__main__":
    main()

