"""Adapter: expose shared food labels to the API."""
try:
    from food_labels import FOOD_LABELS
except ImportError:
    import json
    from pathlib import Path

    _repo_root = Path(__file__).resolve().parents[4]
    _labels_path = _repo_root / "packages" / "shared" / "food_labels.json"
    with open(_labels_path, "r", encoding="utf-8") as _f:
        FOOD_LABELS = json.load(_f)

food_names = FOOD_LABELS
