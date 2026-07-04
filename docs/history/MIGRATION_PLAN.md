# Thai Food Classifier — Monorepo Migration Plan

**For:** Claude Code or GitHub Copilot
**Author of plan:** Plai (with Claude)
**Last updated:** 15 May 2026 (rev. 2 — decisions locked)

---

## 0. How to use this document

You are an AI coding agent. This plan describes a migration from **three separate repositories** to **one production-grade monorepo**. Read this entire document **before** touching any files. Phases are sequential — do not skip ahead. Each phase has explicit acceptance criteria; verify them before moving on.

When you encounter something marked **DECIDE:** ask the human (Plai) before proceeding.
When you encounter something marked **VERIFY:** run the check yourself and report the result.
When you encounter something marked **DO NOT:** that is a hard constraint, not a suggestion.

---

## 1. Context

Plai has three GitHub repositories for the same product (a Thai food image classifier):

| Repo | Role | Stack | Status after migration |
|---|---|---|---|
| `thai-food-image-classification` | Monolithic Flask app + Jinja templates, 80 classes | Flask 2.3.3, TF 2.13, Bootstrap 5 | **Archive** with Git tag `v0-monolith-final` |
| `thai-food-image-classification-api` | REST API backend, 75 classes | Flask 2.0, TF 2.11, MongoDB, Imgur | **Migrate** into new monorepo as `apps/api/` |
| `thai-food-image-classification-web` | Next.js 13 SPA frontend | Next.js 13, React 18, antd, Tailwind | **Migrate** into new monorepo as `apps/web/` |

The monolith (`#1`) is a legacy academic deliverable. The API + Web pair (`#2` + `#3`) is the modern split architecture. We are consolidating `#2` + `#3` into a single monorepo and archiving `#1`.

---

## 2. Definition of Done

The migration is complete when **all** of the following are true:

- [ ] New repo `thai-food-classifier` exists on GitHub with the structure in §4.
- [ ] `apps/web` builds with `pnpm --filter web build` and runs with `pnpm --filter web dev`.
- [ ] `apps/api` runs with `cd apps/api && python index.py` and serves on port 5000.
- [ ] `docker compose up` from repo root brings up Mongo + API + Web locally.
- [ ] Model weights (`MobileNet.h5`, `Xception.h5`) are **NOT** in the Git repo. They are pulled from Hugging Face Hub at runtime.
- [ ] `packages/shared/food_labels.json` is the single source of truth for class labels. Python and TypeScript both consume it.
- [ ] The English label corrections in §6 have been applied.
- [ ] GitHub Actions CI passes for both `apps/web` and `apps/api` on push.
- [ ] CI workflows are path-filtered (frontend-only PRs do not trigger Python builds and vice versa).
- [ ] The contract drift bug in `apps/web/README.md` is fixed (see §7).
- [ ] Repos `#1`, `#2`, `#3` are tagged and archived on GitHub.

---

## 3. Non-goals (DO NOT do these in this migration)

- **DO NOT** retrain the model. Use the existing 75-class weights from repo `#2`.
- **DO NOT** rewrite the Flask API in Node.js / Next.js API routes.
- **DO NOT** replace MongoDB Atlas. The free tier (M0) is fine.
- **DO NOT** replace Imgur image hosting. It works.
- **DO NOT** migrate to Vertex AI / SageMaker endpoints. That is a future phase.
- **DO NOT** add new features. This migration is purely structural.
- **DO NOT** upgrade major versions of Flask, TensorFlow, Next.js, or React in this migration. Lock to current versions.
- **DO NOT** add new dependencies unless explicitly listed in this plan.

---

## 4. Target structure

```
thai-food-classifier/
├── apps/
│   ├── web/                          # from repo #3 (thai-food-image-classification-web)
│   └── api/                          # from repo #2 (thai-food-image-classification-api)
├── packages/
│   └── shared/
│       ├── food_labels.json          # single source of truth for class labels
│       ├── food_labels.py            # Python loader (reads the JSON)
│       └── food_labels.ts            # TypeScript types + loader
├── infra/
│   ├── docker-compose.yml            # local dev: mongo + api + web
│   ├── api.Dockerfile
│   └── web.Dockerfile
├── .github/
│   └── workflows/
│       ├── ci-web.yml                # path filter: apps/web/** + packages/shared/**
│       ├── ci-api.yml                # path filter: apps/api/** + packages/shared/**
│       └── ci-shared.yml             # path filter: packages/shared/**
├── .gitignore
├── pnpm-workspace.yaml
├── package.json                      # root, scripts only
├── README.md
└── CONTRIBUTING.md
```

---

## 5. Phases

### Phase 1 — Initialize the monorepo

**Goal:** Create the new repo with skeleton structure and tooling.

**Steps:**

1. Create a new public GitHub repo named `thai-food-classifier` under Plai's account.
2. Clone it locally.
3. Create the top-level directory tree from §4 (empty placeholder folders are fine).
4. Create `pnpm-workspace.yaml`:
   ```yaml
   packages:
     - "apps/*"
     - "packages/*"
   ```
5. Create a root `package.json` with workspace scripts only:
   ```json
   {
     "name": "thai-food-classifier",
     "private": true,
     "scripts": {
       "dev:web": "pnpm --filter web dev",
       "dev:api": "cd apps/api && python index.py",
       "build:web": "pnpm --filter web build"
     }
   }
   ```
6. Create a comprehensive `.gitignore` (Python + Node + IDE + OS).
7. Create a placeholder root `README.md` (full version comes in Phase 7).

**Acceptance:**
- [ ] `pnpm install` runs without error from repo root (even though apps are empty).
- [ ] Repo is pushed to GitHub.

---

### Phase 2 — Import the API repo

**Goal:** Move repo `#2` into `apps/api/` while preserving as much Git history as is practical.

**Steps:**

1. Clone repo #2 locally. Copy its contents (excluding `.git/`) into `apps/api/`. Do not preserve Git history — per §8 decision 1, originals stay archived on GitHub for blame/history.
2. Inside `apps/api/`:
   - Move `predict.py`, `index.py`, `foodnames.py`, `requirements.txt`, `vercel.json` to their original positions.
   - Keep the `src/` structure if it exists.
   - Keep `tests/`.
   - **DELETE** the `models/` folder contents from Git (we will fetch from Hugging Face). Keep the folder with a `.gitkeep`.
   - Add `models/*.h5` to `.gitignore`.

**Acceptance:**
- [ ] `apps/api/index.py` exists.
- [ ] `apps/api/requirements.txt` exists.
- [ ] No `.h5` files are tracked by Git anywhere in the repo.
- [ ] `cd apps/api && python -c "import index"` runs without crashing (it may fail at runtime due to missing env vars; that's OK for now).

---

### Phase 3 — Import the Web repo

**Goal:** Move repo `#3` into `apps/web/`.

**Steps:**

1. Clone repo #3 locally. Copy its contents (excluding `.git/`) into `apps/web/`.
2. The `package.json` from repo #3 stays inside `apps/web/`. Do not merge it with the root `package.json`.
3. Verify the package name in `apps/web/package.json` is `web` (rename if it's still `image-classification-thaifood`). This is the workspace identifier `pnpm --filter web` uses.

**Acceptance:**
- [ ] `apps/web/package.json` exists with `"name": "web"`.
- [ ] `pnpm install` from repo root installs `apps/web` dependencies.
- [ ] `pnpm --filter web build` completes successfully (it may fail if `NEXT_PUBLIC_API_ENDPOINT` is not set — set it to a dummy value `http://localhost:5000/api` for now).

---

### Phase 4 — Create the shared labels package

**Goal:** Replace `apps/api/foodnames.py` and any hard-coded label lists with a single JSON source of truth in `packages/shared/`.

**Steps:**

1. Create `packages/shared/food_labels.json`. The structure for each entry:
   ```json
   {
     "id": 0,
     "name_th": "ผัดไทย",
     "name_en": "Pad Thai",
     "name_en_alt": []
   }
   ```
2. **VERIFY:** Open `apps/api/foodnames.py` and extract the full list. There must be exactly **75 entries** (per the test `assert len(food_names) == 75` in `apps/api/tests/test_predict.py`). The order of entries determines the class index — it **must match** the order in the source file because the model outputs use this index.
3. Apply the English corrections from §6 of this plan as you build the JSON.
4. Create `packages/shared/food_labels.py`:
   ```python
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
           return json.load(f)

   FOOD_LABELS: list[FoodLabel] = load_labels()
   ```
5. Create `packages/shared/food_labels.ts`:
   ```typescript
   import labels from "./food_labels.json";

   export interface FoodLabel {
     id: number;
     name_th: string;
     name_en: string;
     name_en_alt: string[];
   }

   export const FOOD_LABELS: FoodLabel[] = labels as FoodLabel[];
   ```
6. Update `apps/api/predict.py` to import from `packages/shared/food_labels.py` instead of `foodnames.py`. Use a relative import or add `packages/shared` to `sys.path` at the top of `apps/api/index.py`.
7. **DELETE** `apps/api/foodnames.py` after the API runs successfully against the shared module.
8. Update the test in `apps/api/tests/test_predict.py` to import from the shared module.

**Acceptance:**
- [ ] `packages/shared/food_labels.json` has exactly 75 entries.
- [ ] The first entry's `name_th` matches the first entry of the original `foodnames.py`.
- [ ] `pytest apps/api/tests/` passes.
- [ ] No file in `apps/api/` defines a Thai food name list anymore.

---

### Phase 5 — Migrate model weights to Hugging Face Hub

**Goal:** Remove `MobileNet.h5` and `Xception.h5` from Git. Download them at runtime from Hugging Face Hub.

**Steps:**

1. The Hugging Face repo name is **`PlaiPunlawat/thai-food-classifier`** (locked in §8 decision 2).
2. The human (Plai) must do these steps manually:
   - Sign in at huggingface.co.
   - Create a public model repo with the agreed name.
   - Upload `MobileNet.h5` and `Xception.h5` (the files from the existing local `models/` folder of repo #2) via the web UI or `huggingface-cli upload`.
3. Add `huggingface_hub` to `apps/api/requirements.txt`.
4. Modify `apps/api/predict.py` (or the equivalent service file in `apps/api/src/services/`) to download the model on first use:
   ```python
   from huggingface_hub import hf_hub_download
   import os

   HF_REPO_ID = os.getenv("HF_MODEL_REPO", "PlaiPunlawat/thai-food-classifier")
   _MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "./models")

   def get_model_path(model_name: str) -> str:
       """Returns local path to model weights, downloading from HF Hub if needed."""
       filename = {"xception": "Xception.h5", "mobilenet": "MobileNet.h5"}[model_name]
       return hf_hub_download(
           repo_id=HF_REPO_ID,
           filename=filename,
           cache_dir=_MODEL_CACHE_DIR,
       )
   ```
5. Replace any `load_model("models/Xception.h5")` calls with `load_model(get_model_path("xception"))`.
6. Verify `models/*.h5` is in `.gitignore`. Run `git rm --cached apps/api/models/MobileNet.h5 apps/api/models/Xception.h5` if they were ever tracked.
7. Document the env var `HF_MODEL_REPO` in `apps/api/.env.example`.

**Acceptance:**
- [ ] `git ls-files | grep '\.h5$'` returns nothing.
- [ ] `du -sh apps/api/` is significantly smaller than the original repo size.
- [ ] Starting the API for the first time triggers a one-time download from HF Hub.
- [ ] Second start uses the cached model (no re-download).
- [ ] API still returns predictions correctly for a test image.

---

### Phase 6 — Local dev with docker compose

**Goal:** One command (`docker compose up`) starts MongoDB + API + Web for local development.

**Steps:**

1. Create `infra/api.Dockerfile`:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY apps/api/requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY apps/api/ ./apps/api/
   COPY packages/shared/ ./packages/shared/
   ENV PYTHONPATH=/app
   WORKDIR /app/apps/api
   EXPOSE 5000
   CMD ["python", "index.py"]
   ```
2. Create `infra/web.Dockerfile`:
   ```dockerfile
   FROM node:22-alpine
   WORKDIR /app
   RUN npm install -g pnpm
   COPY pnpm-workspace.yaml package.json ./
   COPY apps/web/package.json ./apps/web/
   RUN pnpm install --frozen-lockfile
   COPY apps/web/ ./apps/web/
   COPY packages/shared/ ./packages/shared/
   WORKDIR /app/apps/web
   EXPOSE 3000
   CMD ["pnpm", "dev"]
   ```
3. Create `infra/docker-compose.yml`:
   ```yaml
   version: "3.8"
   services:
     mongo:
       image: mongo:7
       ports: ["27017:27017"]
       volumes: ["mongo_data:/data/db"]

     api:
       build:
         context: ..
         dockerfile: infra/api.Dockerfile
       ports: ["5000:5000"]
       environment:
         MONGO_URI: mongodb://mongo:27017/
         MONGO_DATABASE: thai_food_api
         IMGUR_CLIENT_ID: ${IMGUR_CLIENT_ID}
         HF_MODEL_REPO: PlaiPunlawat/thai-food-classifier
       depends_on: [mongo]

     web:
       build:
         context: ..
         dockerfile: infra/web.Dockerfile
       ports: ["3000:3000"]
       environment:
         NEXT_PUBLIC_API_ENDPOINT: http://localhost:5000/api
         NEXT_PUBLIC_PUBLIC_BASE_URL: http://localhost:3000
       depends_on: [api]

   volumes:
     mongo_data:
   ```
4. Create `.env.example` at repo root with `IMGUR_CLIENT_ID=`.

**Acceptance:**
- [ ] `cd infra && docker compose up --build` brings up all three services.
- [ ] Browsing to `http://localhost:3000` loads the Next.js app.
- [ ] The app can successfully upload an image and receive a prediction.

---

### Phase 7 — CI workflows

**Goal:** Path-filtered GitHub Actions so frontend PRs don't run TF tests and vice versa.

**Steps:**

1. Create `.github/workflows/ci-api.yml`:
   ```yaml
   name: API CI
   on:
     push:
       paths:
         - "apps/api/**"
         - "packages/shared/**"
         - ".github/workflows/ci-api.yml"
     pull_request:
       paths:
         - "apps/api/**"
         - "packages/shared/**"

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: "3.10"
             cache: "pip"
         - run: pip install -r apps/api/requirements.txt
         - run: pytest apps/api/tests/
           env:
             PYTHONPATH: ${{ github.workspace }}
   ```
2. Create `.github/workflows/ci-web.yml` with similar structure for Next.js (`pnpm install`, `pnpm --filter web lint`, `pnpm --filter web build`).
3. Create `.github/workflows/ci-shared.yml` that triggers on `packages/shared/**` and runs both API and Web checks (since a shared change affects both).

**Acceptance:**
- [ ] Push a PR that only changes `apps/web/**` — only `ci-web` runs.
- [ ] Push a PR that only changes `apps/api/**` — only `ci-api` runs.
- [ ] Push a PR that changes `packages/shared/**` — both run.

---

### Phase 8 — Fix the contract drift bug

**Goal:** Eliminate the documentation drift between API response shape and `apps/web/README.md`.

**Steps:**

1. Open `apps/web/README.md` and find the section under `POST /upload`. The current example response is wrong:
   ```json
   {
     "predict_result": [
       { "food_name": "Tom Yum Kung", "confidence": 0.95 }
     ]
   }
   ```
2. Replace with the **actual** response format (matching what `apps/api/` returns):
   ```json
   {
     "resultId": "507f1f77bcf86cd799439011",
     "predict_result": [
       { "name_en": "Pad Thai", "name_th": "ผัดไทย", "percent": "95.23" }
     ],
     "status": "success",
     "message": "uploaded successfully"
   }
   ```
3. While you're in this file, scan for any other references to `food_name` or `confidence` and replace them.

**Acceptance:**
- [ ] `grep -r "food_name" apps/web/` returns nothing.
- [ ] `grep -r "confidence" apps/web/README.md` returns nothing.

---

### Phase 9 — Write top-level documentation

**Goal:** A new contributor can clone the repo and run it locally in under 10 minutes.

**Steps:**

1. Write `README.md` at the repo root with these sections:
   - One-paragraph project description
   - Architecture diagram (text-based is fine — describe web → api → model/mongo/imgur)
   - Quick start (`docker compose up`)
   - Repo layout (mirror §4 of this plan)
   - Link to `apps/web/README.md` and `apps/api/README.md`
   - Credits to the original academic project (KMITL, Asst. Prof. Dr. Somkiat Wangsiripitak, the team members)
2. Write `CONTRIBUTING.md` covering: branch naming, commit message convention, PR checklist, how to add a new food class (modify `packages/shared/food_labels.json`, retrain model — note this is non-trivial).
3. Update `apps/api/README.md` and `apps/web/README.md` to reflect their new positions in the monorepo. Remove any "clone this repo" instructions; the user clones the monorepo.

**Acceptance:**
- [ ] Root `README.md` exists and is non-trivial (>50 lines).
- [ ] All three READMEs reference the monorepo structure.

---

### Phase 10 — Archive the old repos

**Goal:** Lock the historical repos so they don't drift from the new source of truth.

**Steps for Plai to do manually (after the monorepo is verified working):**

1. In repo `#1` (`thai-food-image-classification`):
   - Add a tag: `git tag v0-monolith-final && git push --tags`.
   - Update its `README.md` first line to say: `> ⚠️ This repository is archived. Active development continues at https://github.com/PlaiPunlawat/thai-food-classifier`.
   - Click GitHub → Settings → Archive this repository.
2. Same for repos `#2` and `#3` — tag as `v1-final` (since they were the production version) and link to the new monorepo.

**Acceptance:**
- [ ] All three old repos show the "Archived" badge on GitHub.
- [ ] All three READMEs link to the new monorepo.

---

## 6. English label corrections to apply in `food_labels.json`

When building `packages/shared/food_labels.json` in Phase 4, apply these corrections to the English translations. The source list is `apps/api/foodnames.py`. Only the entries below need correction — all others keep their existing English wording from `foodnames.py`.

| Thai (`name_th`) | Old `name_en` | Corrected `name_en` | `name_en_alt` |
|---|---|---|---|
| น้ำตก | Thai Grilled Meat Salad | Thai Grilled Meat Salad | `["Nam Tok"]` |
| ต้มข่า | Coconut Soup | Galangal Coconut Soup | `["Tom Kha"]` |
| ต้มยำ | Tom Yum | Tom Yum | `["Tom Yum Goong"]` |
| แกงเทโพ | Morning Glory Curry | Pork Belly Curry with Morning Glory | `["Kaeng Tepo"]` |
| ผัดไท | Pad Thai | Pad Thai | `["ผัดไทย"]` (note: source uses the variant spelling ผัดไท; keep as-is for backward compat) |

**VERIFY before merging:** Plai may want to do a full review of all 75 labels for additional corrections. After Phase 4 produces the initial JSON, generate a markdown table of all 75 entries and present it to Plai for review.

---

## 7. Reference: what's in each source repo

For your context — **do not re-create this; it already exists in the source repos:**

### `apps/api` came from `thai-food-image-classification-api`
- Flask 2.0, TensorFlow 2.11
- MongoDB Atlas for rate-limiting (3 req/min/IP) and result storage
- Imgur for image hosting
- 75 food classes
- Two models: MobileNet (17 MB) and Xception (88 MB)
- Endpoints: `POST /api/upload`, `GET /api/result/<resultId>`, `GET /health`
- Has a `src/` package structure already (services pattern)

### `apps/web` came from `thai-food-image-classification-web`
- Next.js 13, React 18
- antd 5, Tailwind CSS, DaisyUI
- Uses `axios` to call the API
- Pages: `/`, `/predict`, `/about`, `/result/[resultId]`
- One env var matters: `NEXT_PUBLIC_API_ENDPOINT`

---

## 8. Decisions (locked — do not re-ask)

These are confirmed. Do not pause to ask the human about them.

| # | Decision | Value | Notes |
|---|---|---|---|
| 1 | Git history strategy | **Clean copy** (no subtree) | Originals stay archived on GitHub for history. Copy `apps/` contents excluding `.git/`. |
| 2 | Hugging Face repo name | **`PlaiPunlawat/thai-food-classifier`** | Plai creates this manually before Phase 5. |
| 3 | Package manager | **pnpm** | Use `pnpm-workspace.yaml` and `pnpm --filter <name>` filtering. |
| 4 | Python version | **3.10** | TF 2.11 (pinned in repo #2) supports Python 3.7–3.10 officially. Do not use 3.11. |
| 5 | Label review scope | **Apply only the 4 corrections in §6** | Full 75-label review is a separate task. Do not block on it. |

---

## 9. Anti-patterns to watch for

If you find yourself doing any of these, **STOP and ask Plai:**

- Adding new dependencies not listed in this plan
- "Upgrading" Flask, TensorFlow, Next.js, or React versions
- Rewriting `predict.py` logic (only the model path source should change)
- Adding new API endpoints
- Adding new pages to the web app
- Modifying the prediction response shape (`{name_en, name_th, percent}`)
- Removing tests
- Committing `.h5` files
- Committing `.env` files (only `.env.example` should be committed)

---

## 10. When you finish

Open a single pull request titled `feat: initial monorepo migration` against the `main` branch of `thai-food-classifier`. The PR description should:

- Link to this plan
- List which phases were completed
- Flag any deviations from the plan (and why)
- Include the result of running `docker compose up` end-to-end (a screenshot or log paste is fine)

Plai will review and merge. After merge, Phase 10 (archiving the old repos) happens manually.

---

**End of plan.**
