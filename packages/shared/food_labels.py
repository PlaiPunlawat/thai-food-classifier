"""Single source of truth loader for food labels."""
import json
from pathlib import Path
from typing import TypedDict


class FoodLabel(TypedDict):
    id: int
    name_th: str
    name_en: str
    name_en_alt: list[str]


_LABELS_PATH = Path(__file__).parent / "food_labels.json"


def load_labels() -> list[FoodLabel]:
    with open(_LABELS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["labels"]


FOOD_LABELS: list[FoodLabel] = load_labels()
