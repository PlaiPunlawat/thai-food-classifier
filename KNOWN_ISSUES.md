# Known Issues

## Known issues (pre-existing, not caused by migration)

- **tests/test_api.py**: 9 tests reference `index.get_mongo_client` which
  was refactored into `src/services/database_service.py` before the
  monorepo migration. Tests need their mocks updated to patch
  `src.services.database_service.get_mongo_client`. Must be fixed
  before enabling CI in Phase 7.

- ~~**tests/test_predict.py (TestPredictImage)**: 4 tests fail because
  `predict.py` calls `load_model()` at module level.~~ **RESOLVED** in
  Phase 5 — model loading deferred to `PredictionService._load_model()`.

## Resolved in Phase 6

- **TF 2.11 / Keras 3 compat** — resolved by pinning Werkzeug<3.0 and
  related deps in the containerised environment.

- **food_labels import path fragility** — resolved by setting
  `PYTHONPATH=/app:/app/packages/shared` in api.Dockerfile, removing
  brittle `sys.path.insert()` hacks.

## Imgur integration — pending real Client ID

The IMGUR_CLIENT_ID in .env is a placeholder. Browser uploads will
fail at the Imgur step until a real Client ID is registered.

Imgur's app registration flow returned "over capacity" errors during
the migration period (mid-May 2026). Retry later, or migrate off
Imgur entirely.

Future work: Replace Imgur with Cloudinary (free 25 GB) or Cloudflare
R2 (free 10 GB, zero egress). Estimated effort: ~30 min.

## Model file size — Xception.h5 is 333 MB

Larger than originally documented (~88 MB). Likely includes optimizer
state. Future work: re-save with model.save_weights() to drop
optimizer state, ~75% size reduction expected.
