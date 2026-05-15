# Known Issues

## Known issues (pre-existing, not caused by migration)

- **tests/test_api.py**: 9 tests reference `index.get_mongo_client` which
  was refactored into `src/services/database_service.py` before the
  monorepo migration. Tests need their mocks updated to patch
  `src.services.database_service.get_mongo_client`. Must be fixed
  before enabling CI in Phase 7.

- **tests/test_predict.py (TestPredictImage)**: 4 tests fail because
  `predict.py` calls `load_model()` at module level (lines 13–14).
  The test mocks are applied too late — Python evaluates the real
  `load_model` during import before `patch('predict.load_model')` takes
  effect. The models (.h5 files) are not present in the repo, so the
  import crashes with `FileNotFoundError`. Fix: defer model loading
  behind a function or use `importlib` in tests.
