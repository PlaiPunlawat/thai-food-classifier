# Thai Food Classifier — Web Frontend

A Next.js application for uploading food photos and displaying classification results. Supports drag-and-drop, clipboard paste, image cropping, and shareable result URLs.

## Tech Stack

- **Framework:** Next.js 13 (React 18)
- **Styling:** Tailwind CSS, DaisyUI, Ant Design
- **Charts:** Ant Design Charts
- **HTTP Client:** Axios

## Getting Started

This app lives at `apps/web/` within the [thai-food-classifier](../../README.md) monorepo. Uses **pnpm** (not npm or yarn).

### Install dependencies

```bash
# From repo root
pnpm install
```

### Configure environment

```bash
cp .env.example .env.local
```

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `NEXT_PUBLIC_API_ENDPOINT` | Backend API base URL | `http://localhost:5000/api` |
| `NEXT_PUBLIC_PUBLIC_BASE_URL` | Public URL of this app (for sharing) | `http://localhost:3000` |

**Build-time inlining:** Variables prefixed with `NEXT_PUBLIC_` are baked into the JavaScript bundle at `next build` time. Changing them at runtime (e.g., via Docker Compose `environment:`) has no effect on the built output — they must be set as build args in the Dockerfile.

### Development

```bash
pnpm --filter web dev
```

### Production build

```bash
pnpm --filter web build
pnpm --filter web start
```

## Pages

| Route | File | Description |
| ----- | ---- | ----------- |
| `/` | `pages/index.js` | Landing page |
| `/predict` | `pages/predict.js` | Image upload and model selection |
| `/result/[resultId]` | `pages/result/[resultId].js` | Shareable prediction result |
| `/about` | `pages/about.js` | Project information |

## Components

| Component | Purpose |
| --------- | ------- |
| `Navbar.jsx` | Navigation bar |
| `PredictImage.jsx` | Image upload (drag-drop, paste, crop) |
| `PredictResult.jsx` | Result display with chart and top-5 predictions |

## API Contract

The frontend expects the API to return predictions in this shape:

```json
{
  "resultId": "507f1f77bcf86cd799439011",
  "predict_result": [
    { "name_en": "Pad Thai", "name_th": "ผัดไทย", "percent": 95.23 }
  ],
  "status": "success",
  "message": "uploaded successfully"
}
```

Fields per prediction: `name_en` (string), `name_th` (string), `percent` (float, 0–100).

## Project Structure

```text
apps/web/
├── components/
│   ├── Navbar.jsx
│   ├── PredictImage.jsx
│   └── PredictResult.jsx
├── lib/
│   ├── api.js            # Axios instance + API base URL
│   ├── constants.js      # App constants
│   └── utils.js          # Helper functions
├── pages/
│   ├── _app.js           # Global layout and providers
│   ├── index.js          # Landing page
│   ├── predict.js        # Upload page
│   ├── about.js          # About page
│   └── result/
│       └── [resultId].js # Dynamic result page
├── public/               # Static assets (images, fonts)
├── styles/               # Global CSS / Tailwind
├── next.config.js        # Next.js configuration
├── package.json
└── .env.example
```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) in the monorepo root.
