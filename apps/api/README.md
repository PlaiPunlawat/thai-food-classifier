# Thai Food Image Classification API

A REST API that identifies Thai dishes from uploaded images using deep learning. Returns top-5 predictions with Thai and English names and confidence percentages.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/upload` | Upload image for classification |
| GET | `/api/result/<resultId>` | Retrieve stored prediction |
| GET | `/health` | Health check |

### POST /api/upload

Upload an image and receive Thai food predictions.

**Content-Type:** `multipart/form-data`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | File | Yes | Image file (max 5 MB) |
| model | String | No | `mobilenet` or `xception` (default: `xception`) |

**Example:**
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "image=@photo.jpg" \
  -F "model=mobilenet"
```

**Success Response (201):**
```json
{
  "resultId": "507f1f77bcf86cd799439011",
  "predict_result": [
    { "name_en": "Pad Thai", "name_th": "ผัดไทย", "percent": 95.23 },
    { "name_en": "Pad See Ew", "name_th": "ผัดซีอิ๊ว", "percent": 2.15 },
    { "name_en": "Drunken Noodles", "name_th": "ผัดขี้เมา", "percent": 1.42 },
    { "name_en": "Fried Rice", "name_th": "ข้าวผัด", "percent": 0.89 },
    { "name_en": "Tom Yum", "name_th": "ต้มยำ", "percent": 0.31 }
  ],
  "status": "success",
  "message": "uploaded successfully"
}
```

Response fields: `name_en` (string), `name_th` (string), `percent` (float, 0–100, 2 dp).

**Error Responses:**
- `400` — Missing image file or empty filename
- `429` — Rate limit exceeded (3 requests per IP per minute)
- `413` — Image exceeds 5 MB
- `500` — Internal server error

### GET /api/result/:resultId

**Success Response (200):**
```json
{
  "status": "success",
  "predict_result": [
    { "name_en": "Pad Thai", "name_th": "ผัดไทย", "percent": 95.23 }
  ],
  "image_url": "https://i.imgur.com/abc123.jpg"
}
```

`image_url` is `null` when Imgur is not configured.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGO_URI` | Yes | `mongodb://localhost:27017/` | MongoDB connection string |
| `MONGO_DATABASE` | No | `thai_food_api` | Database name |
| `IMGUR_CLIENT_ID` | No | (empty) | Imgur API client ID; uploads skipped if unset |
| `HF_MODEL_REPO` | No | `PlaiPunlawat/thai-food-classifier` | Hugging Face repo for model weights |
| `FLASK_ENV` | No | `development` | Flask environment |
| `FLASK_DEBUG` | No | `False` | Enable debug mode (local dev only) |

## Models

| Model | File | Download Size | Input Size | Notes |
|-------|------|--------------|------------|-------|
| MobileNet | `MobileNet.h5` | ~44 MB | 128×128 | Faster inference |
| Xception | `Xception.h5` | ~333 MB | 128×128 | Higher accuracy |

Weights are downloaded from Hugging Face Hub on first prediction and cached in `models/`. In Docker, the `hf_models` volume persists weights across container restarts.

## Local Development (without Docker)

Prerequisites: Python 3.10, MongoDB running locally.

```bash
cd apps/api

# Install uv if not already installed
# See https://docs.astral.sh/uv/getting-started/installation/

# Install dependencies
uv sync

# Run the dev server
uv run python index.py
```

Set `PYTHONPATH` to include the repo root and shared package:
```bash
export PYTHONPATH=/path/to/thai-food-classifier:/path/to/thai-food-classifier/packages/shared
```

## Running Tests

```bash
cd apps/api
uv sync --dev
uv run pytest tests/ -v
```

Tests run without network, MongoDB, or model files — all external dependencies are mocked.

## Project Structure

```
apps/api/
├── index.py                # Flask app entry point + route registration
├── src/
│   ├── api/
│   │   └── routes.py       # Request handling, validation, orchestration
│   ├── config/
│   │   ├── settings.py     # Environment-based configuration
│   │   └── food_names.py   # Adapter over packages/shared/food_labels.json
│   ├── services/
│   │   ├── prediction_service.py  # Model loading, preprocessing, inference
│   │   ├── database_service.py    # MongoDB operations, rate limiting
│   │   └── image_service.py       # Imgur upload
│   └── utils/
│       └── logger.py       # Logging setup
├── tests/                  # pytest test suite (23 tests)
├── models/                 # .gitignored; populated from HF Hub at runtime
├── pyproject.toml          # Dependencies and tool config
└── uv.lock                 # Deterministic dependency lockfile
```

## Rate Limiting

3 requests per IP address per minute, tracked in MongoDB. Note: behind a reverse proxy, all requests may appear from the gateway IP (see [KNOWN_ISSUES.md](../../KNOWN_ISSUES.md)).

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) in the monorepo root.
