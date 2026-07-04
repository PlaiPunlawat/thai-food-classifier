# Contributing

## Branch Naming

```
feat/short-description    # New features
fix/short-description     # Bug fixes
docs/short-description    # Documentation changes
refactor/short-description # Code refactoring
build/short-description   # Build system / dependency changes
ci/short-description      # CI workflow changes
```

## Commit Messages

This project uses conventional commits:

```
feat: add new food class to shared labels
fix: correct prediction percentage formatting
docs: update API endpoint documentation
ci: add lint step to web workflow
build: migrate api to uv with locked dependencies
refactor: extract model loading into service
```

Format: `<type>: <short description in imperative mood>`

## Dependency Workflow (API)

The API uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Edit dependencies in `apps/api/pyproject.toml`
2. Run `cd apps/api && uv lock` to regenerate the lockfile
3. Commit **both** `pyproject.toml` and `uv.lock` together
4. CI validates the lockfile with `uv sync --locked` — if the lockfile
   is out of sync with pyproject.toml, CI will fail

Do not edit `uv.lock` by hand.

## Dependency Workflow (Web)

The web app uses pnpm.

1. Run `pnpm --filter web add <package>` from the repo root
2. Commit the updated `package.json` and `pnpm-lock.yaml`

## Pull Request Checklist

Before submitting a PR, verify:

- [ ] CI is green (relevant workflow passes)
- [ ] No `.h5` model files are committed (`git ls-files | grep '\.h5$'` returns nothing)
- [ ] No `.env` files are committed (only `.env.example` is tracked)
- [ ] `uv.lock` is in sync with `pyproject.toml` (`cd apps/api && uv sync --locked` succeeds)
- [ ] Preprocessing pipeline unchanged (guard test passes: `uv run pytest apps/api/tests/test_prediction_service.py -k preprocess`)
- [ ] API response contract is consistent across `apps/api/` source, `apps/api/README.md`, and `apps/web/README.md` (fields: `name_en`, `name_th`, `percent`)
- [ ] Changes to `packages/shared/food_labels.json` do not alter entry order (order determines model class index)

## Adding a New Food Class

High-level steps:

1. Add the new entry to `packages/shared/food_labels.json` with the next sequential `id`
2. Retrain both models (MobileNet and Xception) with the new class included
3. Upload updated `.h5` weights to the Hugging Face Hub repo
4. Update tests to reflect the new class count

Retraining is non-trivial and requires the original training dataset and pipeline. This is not documented here.
