# Known Issues

## Known issues (pre-existing, not caused by migration)

- **tests/test_api.py**: 9 tests reference `index.get_mongo_client` which
  was refactored into `src/services/database_service.py` before the
  monorepo migration. Tests need their mocks updated to patch
  `src.services.database_service.get_mongo_client`. Must be fixed
  before enabling CI in Phase 4.

- ~~**tests/test_predict.py (TestPredictImage)**: 4 tests fail because
  `predict.py` calls `load_model()` at module level.~~ **RESOLVED** in
  Phase 5 — model loading deferred to `PredictionService._load_model()`.

## Resolved in Phase 6

- **TF 2.11 / Keras 3 compat** — resolved by pinning Werkzeug<3.0 and
  related deps in the containerised environment.

- **food_labels import path fragility** — resolved by setting
  `PYTHONPATH=/app:/app/packages/shared` in api.Dockerfile, removing
  brittle `sys.path.insert()` hacks.

## Resolved in Phase 1

- ~~**API crashes at startup: food_names import**~~ — `food_names.py`
  rewritten as a thin adapter over `packages/shared/food_labels.json`
  (the SSOT). Prediction service now indexes a list of dicts correctly.
  Label order verified to match the legacy numpy array.

- ~~**No model download code**~~ — `PredictionService._load_model()` now
  downloads from Hugging Face Hub (`PlaiPunlawat/thai-food-classifier`)
  on first prediction if `.h5` file is missing. `huggingface_hub` added
  to dependencies.

- ~~**Imgur upload unconditional**~~ — upload is now skipped when
  `IMGUR_CLIENT_ID` is unset or empty; failures are caught and logged
  without killing the prediction. `image_url` is `null` in that case.

## Imgur integration — pending real Client ID

The IMGUR_CLIENT_ID in .env is a placeholder. Predictions will succeed
with `image_url: null` until a real Client ID is registered.

Future work: Replace Imgur with Cloudinary (free 25 GB) or Cloudflare
R2 (free 10 GB, zero egress). Estimated effort: ~30 min.

## Preprocessing divergence (D5 — awaiting human verification)

Legacy `predict.py` applies `xception.preprocess_input` **then** `/255`
(double-scaling). The current `PredictionService` applies only `/255`.
Which matches the original training is unverified. Plai must check the
training notebook; if unavailable, empirically compare both paths on
5–10 known dish photos and keep whichever gives sane top-1 accuracy.

## Model file size — Xception.h5 is 333 MB

Larger than originally documented (~88 MB). Likely includes optimizer
state. Future work: re-save with model.save_weights() to drop
optimizer state, ~75% size reduction expected.
