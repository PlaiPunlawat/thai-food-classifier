# packages/shared

Single source of truth for Thai food class labels used by both the API (Python) and web frontend (TypeScript).

## Class count: 72

The model's Xception.h5 output layer has 72 units, confirmed via `h5py` inspection. Earlier documentation and test assertions referenced 75 classes — this was stale and never matched the actual model. The true count is 72.

## Files

- `food_labels.json` — flat array of 72 `FoodLabel` objects, ordered by class index
- `food_labels.py` — Python loader exposing `FOOD_LABELS: list[FoodLabel]`
- `food_labels.ts` — TypeScript types and re-export
