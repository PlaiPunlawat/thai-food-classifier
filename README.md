# Thai Food Classifier

![Demo](docs/images/demo.png)
<!-- TODO(Plai): capture upload→result screenshot, save to
docs/images/demo.png, then delete this comment -->

A monorepo for the Thai food image classification system. Upload a photo of a Thai dish and the application identifies it using deep learning (MobileNet or Xception), returning the dish name in Thai and English along with prediction percentages. The system classifies 72 Thai dishes and stores results for sharing via unique URLs.

## Architecture

```
┌─────────────┐       ┌─────────────────┐       ┌────────────────┐
│  Next.js    │       │   Flask API     │       │   MongoDB      │
│  Frontend   │──────▶│   (port 5000)   │──────▶│   (port 27017) │
│  (port 3000)│       │                 │       └────────────────┘
└─────────────┘       │                 │
                      │                 │──────▶ Imgur (image hosting)
                      │                 │
                      │                 │──────▶ Hugging Face Hub
                      │                 │        (model weights)
                      └─────────────────┘
```

- **Web** (Next.js 13, React 18) — image upload UI, result display, shareable URLs
- **API** (Flask 2.0, TensorFlow 2.11) — classification inference, rate limiting, result storage
- **Models** — MobileNet (~44 MB) and Xception (~333 MB), downloaded from Hugging Face Hub at runtime

## Quick Start

Prerequisites: Docker and Docker Compose installed.

```bash
# Clone the repository
git clone https://github.com/PlaiPunlawat/thai-food-classifier.git
cd thai-food-classifier

# Copy environment file and add your Imgur Client ID (optional)
cp .env.example .env

# Start all services (MongoDB + API + Web)
cd infra
docker compose up --build -d
```

Once running:

- Frontend: <http://localhost:3000> (production build served by `next start`)
- API: <http://localhost:5000> (gunicorn, 1 worker + 4 threads)
- MongoDB: localhost:27017

**First prediction** triggers a one-time model download from Hugging Face Hub
into a persistent Docker volume (`hf_models`). MobileNet is ~44 MB; Xception
is ~333 MB. Subsequent container restarts reuse the cached weights — no
re-download occurs.

See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for current limitations including the Imgur placeholder.

## Repo Layout

```
thai-food-classifier/
├── apps/
│   ├── web/                    # Next.js frontend
│   └── api/                    # Flask API backend
├── packages/
│   └── shared/
│       ├── food_labels.json    # Single source of truth for 72 class labels
│       ├── food_labels.py      # Python loader
│       └── food_labels.ts      # TypeScript types + loader
├── infra/
│   ├── docker-compose.yml      # Local dev: mongo + api + web
│   ├── api.Dockerfile
│   └── web.Dockerfile
├── .github/
│   └── workflows/
│       ├── ci-web.yml          # Path-filtered: apps/web/** + packages/shared/**
│       ├── ci-api.yml          # Path-filtered: apps/api/** + packages/shared/**
│       └── ci-shared.yml       # Triggers both on packages/shared/** changes
├── .gitignore
├── pnpm-workspace.yaml
├── package.json
└── README.md
```

## App Documentation

- [apps/web/README.md](apps/web/README.md) — Frontend setup, environment variables, project structure
- [apps/api/README.md](apps/api/README.md) — API endpoints, model info, deployment notes

## Engineering Notes

### Monorepo consolidation

This project was originally three standalone repositories: a monolithic Flask+Jinja app (archived), a Flask REST API, and a Next.js frontend. They were consolidated into a single pnpm workspace monorepo to enforce a shared label contract, run path-filtered CI from one place, and provide a one-command local setup (`docker compose up`).

### Single source of truth for labels

[packages/shared/food_labels.json](packages/shared/food_labels.json) defines all 72 dish classes. Both the Python API and TypeScript frontend import from this file. Entry order is the model class index — reordering entries silently breaks predictions. This invariant is enforced by `test_labels.py` and a CONTRIBUTING checklist rule.

### Lazy model loading via Hugging Face Hub

Model weights (`.h5` files) are never stored in Git. On first prediction, `PredictionService` downloads the requested model from the `PlaiPunlawat/thai-food-classifier` Hugging Face repo into a persistent Docker volume (`hf_models`). Subsequent container restarts reuse the cached weights.

### Preprocessing quirk (double-scaling)

The original 2022 training pipeline applied `xception.preprocess_input` (which maps pixels to [-1, 1]) **followed by** `/255`. This produces inputs in the range [-1/255, 1/255] — an unconventional transform, but the model weights depend on it. Inference must replicate it exactly. A regression test in `test_prediction_service.py` pins the expected input range; removing the double-scaling makes predictions confidently wrong. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md) for details.

### Dependency determinism (pip → uv)

Migrating from pip/requirements.txt to uv with a lockfile exposed a ghost dependency: `keras-nightly` had coexisted with `keras==2.11.0` since 2022 because pip overwrites conflicting namespace files in installation order. uv's deterministic linking surfaced the conflict immediately. The fix was removing the dead package — it was a pip-freeze artifact never actually needed.

### Serving architecture

The API runs under gunicorn with **1 worker × 4 threads**. A single worker loads the TensorFlow model once (~1 GB in RAM); threads share that loaded model across concurrent requests. The `--timeout 300` flag prevents gunicorn from killing the worker during first-run model downloads (MobileNet ~44 MB, Xception ~333 MB).

### Testing approach

All 23 tests run without network, MongoDB, or model files. Mocks patch at the import site (not the source module), which is necessary because Python's `from X import Y` creates a binding in the importing module's namespace. The preprocessing guard test asserts input values fall in [-1/255, 1/255] — it exists specifically to catch well-meaning "cleanup" of the double-scaling.

## Project History

Planning artifacts from the 2026 refactor are preserved in [docs/history/](docs/history/).

## Credits

This project was developed as part of **Project in Data Science and Business Analytics 2** (Course Code: 06026128), 1st semester of academic year 2022, at the School of Information Technology, King Mongkut's Institute of Technology Ladkrabang (KMITL).

**Team Members:**
- Punlawat Leecharoen
- Smith Cheablam

**Advisor:**
- Asst. Prof. Dr. Somkiat Wangsiripitak — School of Information Technology, KMITL
