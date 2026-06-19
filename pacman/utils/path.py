from pathlib import Path
import sys


def asset_path(relative_path: str) -> str:
    meipass = getattr(sys, "_MEIPASS", None)

    if meipass:
        base_path = Path(meipass) / "assets"
    else:
        base_path = Path(__file__).resolve().parents[2] / "assets"

    return str(base_path / relative_path)
