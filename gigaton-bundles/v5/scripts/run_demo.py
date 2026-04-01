import json
import subprocess
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parents[1]
    demo_dir = root / "demo_output"
    demo_dir.mkdir(exist_ok=True)

    subprocess.run([
        sys.executable,
        str(root / "scripts" / "generate_namespace.py"),
        str(root / "examples" / "sample_client_intake.json"),
        str(root / "memory_registry.v5.json"),
        str(demo_dir / "namespace"),
        "client_liquefex_demo"
    ], check=True)

    subprocess.run([
        sys.executable,
        str(root / "scripts" / "calibrate_retrieval.py"),
        str(root / "retrieval_scoring_calibration.json"),
        str(root / "examples" / "sample_retrieval_feedback.json"),
        str(demo_dir / "calibration")
    ], check=True)

    print("[OK] Demo completed")

if __name__ == "__main__":
    main()
