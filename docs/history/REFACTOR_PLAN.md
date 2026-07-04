# thai-food-classifier — Refactor & Repair Plan

Target repo: https://github.com/PlaiPunlawat/thai-food-classifier
Execution model: Claude Code (one phase = one session = one PR).
Rule for the executor: **complete a phase, run its verification commands, confirm green, then stop.** Do not combine phases. Do not refactor beyond the phase scope.

---

## Current-state findings (from audit, 2026-07-04)

| # | Issue | Severity | Evidence |
|---|-------|----------|----------|
| 1 | API crashes at startup: `prediction_service.py` imports `food_names` (list of dicts) from `src/config/food_names.py`, which only defines `FOOD_NAME` (legacy numpy array) | Blocker | `apps/api/src/services/prediction_service.py` line ~6 vs `apps/api/src/config/food_names.py` |
| 2 | No Hugging Face model download code exists; README + docker-compose claim runtime download. `huggingface_hub` not in requirements. First predict → `FileNotFoundError` | Blocker | `settings.py` ignores `HF_MODEL_REPO` env |
| 3 | API↔Web response contract mismatch: API returns `name_en`/`name_th`/`percent`; web reads `item.name`/`item.confident` | Blocker | `apps/web/components/PredictResult.jsx` lines 47, 51, 110 |
| 4 | Three sources of truth for labels: `apps/api/foodnames.py`, `apps/api/src/config/food_names.py` (byte-identical copies), `packages/shared/food_labels.json` (intended SSOT, unused by API) | High | file sizes identical (5304 B) |
| 5 | Imgur upload is unconditional; placeholder client ID → every upload returns 500 | High | `routes.py` calls `image_service.upload_to_imgur` with no fallback |
| 6 | Tests broken: `test_api.py` mocks `index.get_mongo_client` (moved to `database_service`); root `ci-api.yml` runs pytest on push → CI permanently red | High | documented in KNOWN_ISSUES.md |
| 7 | Legacy standalone-repo artifacts inside `apps/api/`: nested `.github/workflows/` (dead — GitHub only runs root workflows), `vercel.json`, `setup.py`, `MANIFEST.in`, `predict.py`, `foodnames.py` | Medium | tree listing |
| 8 | Dependencies declared 3× (`requirements.txt`, `pyproject.toml`, `setup.py`) — already drifting risk | Medium | |
| 9 | Two JS lockfiles: `apps/web/yarn.lock` + root `pnpm-lock.yaml` | Medium | |
| 10 | Preprocessing divergence: legacy `predict.py` = xception `preprocess_input` **then** `/255` (double-scaling, likely an original bug); new service = `/255` only. Which matches training is unverified → silent accuracy risk | Medium — needs human verification | |
| 11 | `web.Dockerfile` runs `pnpm dev` (dev server) as the container command | Low | |
| 12 | Duplicate per-app `.gitignore`/`.gitattributes`/`CONTRIBUTING.md`; `.env.example` duplicated at root and per-app with different keys | Low | |

---

## Decisions required from Plai before starting (answer inline, executor reads these)

- **D1 — Response contract:** standardize on `{ name_en, name_th, percent }` where `percent` is a **number** (float, 0–100, 2 dp), not a string. → DECIDED unless changed: yes.
- **D2 — Image hosting:** Phase 1 makes Imgur **optional** (skip on missing key, `image_url: null`). Permanent replacement (Cloudinary / Cloudflare R2 / drop the feature) is deferred to Phase 7 stretch. → Default: keep optional.
- **D3 — Framework:** keep Flask + TF 2.11 pinned. Do NOT upgrade to Keras 3 / FastAPI in this plan (`.h5` loading compat risk; scope creep). FastAPI migration = separate future project.
- **D4 — Python packaging:** single `pyproject.toml`, managed with `uv`. `requirements.txt` becomes generated (`uv export`) or deleted with Dockerfile switched to uv. → Default: switch Dockerfile to uv, delete requirements files.
- **D5 — Preprocessing (issue #10):** Plai must check the original training notebook. If unavailable, empirically compare both preprocessing paths on 5–10 known dish photos and keep whichever gives sane top-1. Record the answer in KNOWN_ISSUES.md. **This is a human task — the executor must not guess.**

---

## Phase 1 — Make the API boot and predict (blockers #1, #2, #5)

Scope: `apps/api` only.

1. **Fix label import (SSOT).**
   - Rewrite `apps/api/src/config/food_names.py` as a thin adapter over the shared package:
     ```python
     """Adapter: expose shared food labels to the API."""
     from food_labels import FOOD_LABELS  # resolved via PYTHONPATH=/app/packages/shared

     food_names = FOOD_LABELS  # list[{"id", "name_th", "name_en", "name_en_alt"}]
     ```
   - For local (non-Docker) dev, add a fallback path insert guarded by try/except ImportError that loads `packages/shared/food_labels.json` relative to repo root. Keep it small.
   - Confirm `prediction_service.py` indexing (`food_names[idx]['name_en']`) works against the JSON schema. **Verify JSON order matches the legacy numpy array order** (order = model class index). Write a one-off comparison script, run it, then delete it — or add it as a permanent test in Phase 4.
2. **Add model download from HF Hub.**
   - Add `huggingface_hub` to dependencies.
   - In `settings.py`: read `HF_MODEL_REPO` env (default `PlaiPunlawat/thai-food-classifier`).
   - In `PredictionService._load_model`: if the `.h5` file is missing locally, download via `hf_hub_download(repo_id=Config.HF_MODEL_REPO, filename="MobileNet.h5" | "Xception.h5", local_dir=Config.MODEL_PATH)`. Log download start/finish.
   - First verify the actual filenames on the HF repo (`huggingface_hub.list_repo_files`) — do not assume.
3. **Make Imgur optional.**
   - In `routes.py`: only call `image_service.upload_to_imgur` if `Config.IMGUR_CLIENT_ID` is set and non-empty; else `image_url = None` and log a warning.
   - Wrap the Imgur call in try/except: on failure, log and continue with `image_url = None` (a hosting outage must not kill prediction).
4. Update `KNOWN_ISSUES.md`: mark resolved items, add D5 preprocessing question if still open.

**Acceptance criteria**
```bash
cd infra && docker compose up --build -d
curl -f http://localhost:5000/health
# predict with any jpg, mobilenet first (17 MB download, fast):
curl -f -X POST -F "image=@test.jpg" -F "model=mobilenet" http://localhost:5000/api/upload
# → 201, JSON contains predict_result[0].name_en and name_th; no 500
```

---

## Phase 2 — Unify the API↔Web contract (blocker #3)

Scope: `apps/api` response shape + `apps/web` consumers.

1. API: in `prediction_service.py`, return `percent` as **float** (e.g. `round(confidence, 2)`), per D1. Confirm `save_result`/`get_result` round-trip the same shape.
2. Web: update every consumer to the new contract:
   - `components/PredictResult.jsx` — replace `item.name` → `item.name_en`, `item.confident` → `item.percent` (all occurrences: headline, chart data mapping, the `> 80` threshold, annotation match).
   - `components/PredictImage.jsx` and `pages/result/[resultId].js` — grep for `confident` and `.name` usages and fix.
3. Grep the whole repo for the old field names; zero remaining references outside git history:
   ```bash
   grep -rn "confident" apps/web apps/api --include="*.js*" --include="*.py" | grep -v node_modules
   ```
4. Update `apps/api/README.md` and `apps/web/README.md` response-contract sections to match.

**Acceptance criteria**
- `docker compose up` → upload a photo through the browser at localhost:3000 → result page shows dish name (TH + EN) and percentages, chart renders.
- Contract documented identically in both READMEs (matches the CONTRIBUTING.md checklist item).

---

## Phase 3 — Delete legacy artifacts (issues #4, #7, #9, #12)

Scope: deletions + small reference fixes only. No behavior change.

Delete:
- `apps/api/foodnames.py`
- `apps/api/predict.py` (superseded by `PredictionService`; its tests are rewritten in Phase 4)
- `apps/api/.github/` (entire nested workflows dir — dead code)
- `apps/api/vercel.json`, `apps/api/setup.py`, `apps/api/MANIFEST.in`
- `apps/api/.gitattributes`, `apps/api/.gitignore` (fold needed patterns into root `.gitignore`)
- `apps/api/CONTRIBUTING.md` (fold anything unique into root `CONTRIBUTING.md`; keep `apps/api/LICENSE` → move to repo root as `LICENSE` if root has none)
- `apps/web/yarn.lock`, `apps/web/.eslintrc.json` only if config is duplicated elsewhere — otherwise keep eslint config
- `apps/api/tests/test_predict.py` sections that test the deleted `predict.py` (full rewrite lands in Phase 4; deleting dead tests here is fine)

Then:
- `grep -rn "foodnames\|from predict import\|import predict" apps/ packages/` → zero hits.
- Root `.gitignore` covers: `models/*.h5`, `.env`, `__pycache__/`, `.next/`, `node_modules/`, coverage artifacts.

**Acceptance criteria**
- `docker compose up --build` still works end-to-end (rebuild from scratch: `docker compose build --no-cache api`).
- Zero references to deleted files.

---

## Phase 4 — Fix the test suite (issue #6)

Scope: `apps/api/tests` + shared-label test.

1. `tests/test_api.py`: update all mocks from `index.get_mongo_client` → patch `src.services.database_service.database_service` methods (`check_rate_limit`, `log_request`, `save_result`, `get_result`). Prefer patching the singleton's methods over module internals.
2. Rewrite `tests/test_predict.py` against `PredictionService`:
   - Mock `_load_model` to return a fake model whose `.predict` returns a fixed 72-dim probability vector.
   - Assert: top-5 ordering, contract keys (`name_en`, `name_th`, `percent`), `percent` is float, invalid `model` param falls back correctly.
3. Add `tests/test_labels.py`: assert `len(food_names) == 72`, ids are `0..71` in order, and (if the Phase 1 comparison script was kept) that JSON order matches the legacy array order snapshot.
4. Ensure tests pass with `PYTHONPATH` matching CI (`repo_root:repo_root/packages/shared`).

**Acceptance criteria**
```bash
PYTHONPATH=$PWD:$PWD/packages/shared pytest apps/api/tests/ -v
# all green, no skips masking failures
```

---

## Phase 5 — Dependency hygiene with uv (issue #8, decision D4)

Scope: `apps/api` packaging + `infra/api.Dockerfile` + `ci-api.yml`.

1. Rewrite `apps/api/pyproject.toml`:
   - Keep runtime deps pinned as-is (TF 2.11, Flask 2.0 stack — D3). Add `huggingface_hub` from Phase 1. Keep the `Werkzeug<3.0` pin noted in KNOWN_ISSUES (add explicitly if not present).
   - Move dev deps to `[dependency-groups] dev` (uv convention) or keep `[project.optional-dependencies].dev`.
   - Remove `[build-system]`/setuptools packaging metadata not needed for an app (it is not a published package).
2. Generate `uv.lock` (`uv lock`). Delete `requirements.txt` and `requirements-dev.txt`.
3. `infra/api.Dockerfile`: install uv (`COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv`), then `uv sync --frozen --no-dev`. Note: verify current uv syntax against uv docs at execution time — flags change between versions.
4. `.github/workflows/ci-api.yml`: use `astral-sh/setup-uv` action, `uv sync --frozen`, `uv run pytest apps/api/tests/ -v` with the correct `PYTHONPATH` env. Update `cache-dependency-path` to `apps/api/uv.lock`.

**Acceptance criteria**
- `docker compose build --no-cache api && docker compose up` works.
- CI run on a PR branch is green for `ci-api.yml`.
- `git ls-files | grep requirements` → empty.

---

## Phase 6 — Production-shaped containers (issue #11)

Scope: `infra/` only.

1. `api.Dockerfile`: run under gunicorn (`gunicorn -w 1 --threads 4 -b 0.0.0.0:5000 index:app`) — **1 worker** intentionally, so the TF model loads once (each gunicorn worker would hold its own ~1 GB+ TF session). Add gunicorn to deps.
2. `web.Dockerfile`: multi-stage — stage 1 `pnpm install` + `pnpm --filter web build`; stage 2 copy `.next` + run `pnpm --filter web start`. Respect `.nvmrc` (node 22).
3. `docker-compose.yml`: add `healthcheck` on api (`curl -f http://localhost:5000/health`), `depends_on: condition: service_healthy` for web→api, named volume for HF model cache so weights survive container rebuilds (`hf_models:/app/apps/api/models`).
4. Root `README.md`: update Quick Start if commands changed; add a "first request downloads ~17 MB / ~333 MB" note per model.

**Acceptance criteria**
- Cold `docker compose up --build`: web serves the **built** app on 3000, api healthcheck green, second `up` does not re-download models.

---

## Phase 7 — Docs & portfolio polish (+ stretch items)

1. Root `README.md`: add a screenshot or short GIF of the upload→result flow; add a short "Engineering notes" section (monorepo layout rationale, SSOT labels, lazy model loading, why TF pinned). This is the portfolio payload.
2. Resolve D5 (preprocessing) and record the conclusion in `KNOWN_ISSUES.md` or delete the entry if fixed.
3. Update `CONTRIBUTING.md` PR checklist to reflect current reality (uv, contract fields, no requirements.txt).
4. Stretch (separate PRs, optional):
   - Replace Imgur with Cloudflare R2 or store thumbnails in Mongo GridFS (D2).
   - Re-save Xception weights without optimizer state (~333 MB → ~85 MB per KNOWN_ISSUES estimate).
   - Rate limiting: respect `X-Forwarded-For` behind a proxy; make limits configurable via env.
   - Next.js upgrade (13 → current) — high effort, low portfolio ROI; recommend skipping.

---

## Executor ground rules (paste into CLAUDE.md or the session prompt)

- One phase per session. Read this plan file first; read `KNOWN_ISSUES.md` second.
- Never commit `.h5` files or `.env` (enforced by CONTRIBUTING checklist).
- Never reorder `packages/shared/food_labels.json` entries — order is the model class index.
- When touching the response contract, update: API code, both app READMEs, web consumers, and tests — in the same PR.
- Pinned versions (TF 2.11 / Flask 2.0 / Keras 2.11) are intentional. Do not "helpfully" upgrade.
- If a verification command fails, fix within phase scope or stop and report — do not widen scope.
- Conventional commits per root CONTRIBUTING.md (`feat:`, `fix:`, `refactor:`, `docs:`, `ci:`).
