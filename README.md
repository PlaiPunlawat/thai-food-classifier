# Thai Food Classifier

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
- **Models** — MobileNet (~17 MB) and Xception (~333 MB), downloaded from Hugging Face Hub at runtime

## Quick Start

Prerequisites: Docker and Docker Compose installed.

```bash
# Clone the repository
git clone https://github.com/PlaiPunlawat/thai-food-classifier.git
cd thai-food-classifier

# Copy environment file and add your Imgur Client ID
cp .env.example .env

# Start all services (MongoDB + API + Web)
cd infra
docker compose up --build
```

Once running:

- Frontend: <http://localhost:3000>
- API: <http://localhost:5000>
- MongoDB: localhost:27017

On first API request, model weights are downloaded from Hugging Face Hub (one-time, cached locally).

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

## Credits

This project was developed as part of **Project in Data Science and Business Analytics 2** (Course Code: 06026128), 1st semester of academic year 2022, at the School of Information Technology, King Mongkut's Institute of Technology Ladkrabang (KMITL).

**Team Members:**
- Punlawat Leecharoen
- Smith Cheablam

**Advisor:**
- Asst. Prof. Dr. Somkiat Wangsiripitak — School of Information Technology, KMITL
