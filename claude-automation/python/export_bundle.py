from __future__ import annotations
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def build_zip(output_path: Path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in ROOT.rglob("*"):
            if p == output_path:
                continue
            zf.write(p, p.relative_to(ROOT.parent))

if __name__ == "__main__":
    out = ROOT.parent / "claude-automation-thread-package.zip"
    build_zip(out)
    print(f"Wrote {out}")
