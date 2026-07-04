# Known Issues

## Permanent invariants

**Preprocessing double-scaling — DO NOT CHANGE.**
The original 2022 training pipeline applied `xception.preprocess_input`
(maps pixels to [-1, 1]) **then** `/255`. This produces inputs in
[-1/255, 1/255]. The model weights depend on this exact transform.
Verified empirically 04 Jul 2026: predictions are confidently wrong
without the double-scaling. A regression test in
`apps/api/tests/test_prediction_service.py` pins the expected range.
Do NOT normalize to a single scaling step.

## Open issues

- **Imgur Client ID is a placeholder.** Predictions succeed with
  `image_url: null` until a real Client ID is registered at
  <https://api.imgur.com/oauth2/addclient>. Future work: replace Imgur
  with Cloudflare R2 (free 10 GB, zero egress) or Cloudinary (free 25 GB).

- **Xception.h5 is 333 MB (includes optimizer state).** Expected size
  without optimizer state is ~85 MB. Future work: re-save with
  `model.save_weights()` to drop optimizer state (~75% size reduction).

- **Rate limiter uses `request.remote_addr`.** Behind a reverse proxy
  (nginx, Cloudflare), all requests appear from the gateway IP. Future
  work: respect `X-Forwarded-For` and make limits configurable via env.

## Resolved (archive)

- API crashes at startup due to `food_names` import mismatch — fixed by
  rewriting `food_names.py` as adapter over `packages/shared/food_labels.json`.
- No model download code existed — added HF Hub download in `PredictionService._load_model()`.
- Imgur upload was unconditional — made optional (skipped when `IMGUR_CLIENT_ID` unset).
- API-Web response contract mismatch (`item.name`/`item.confident` vs
  `name_en`/`name_th`/`percent`) — unified across API, web, and both READMEs.
- Legacy standalone-repo artifacts (nested `.github/`, `vercel.json`, `setup.py`,
  duplicate lockfiles) — deleted in cleanup phase.
- Test suite broken (9 tests referenced moved `index.get_mongo_client`) — all 23
  tests rewritten to patch singletons at import site.
- Dependencies declared 3x (`requirements.txt`, `pyproject.toml`, `setup.py`) —
  consolidated to single `pyproject.toml` + `uv.lock`.
- `web.Dockerfile` ran `pnpm dev` in production — replaced with multi-stage build
  and `next start`.
- TF 2.11 / Keras compat issues — resolved by pinning deps and removing ghost
  `keras-nightly` dependency.
- `food_labels` import path fragility — resolved via `PYTHONPATH` in Dockerfile.
