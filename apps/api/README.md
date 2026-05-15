# Thai Food Image Classification API

A REST API service that uses deep learning to automatically identify Thai dishes from uploaded images. The API leverages pre-trained Keras/TensorFlow models (MobileNet and Xception) to classify 75 different Thai food dishes with confidence scores.

## Features

- **Deep Learning Classification**: Uses state-of-the-art CNN models (MobileNet/Xception)
- **Dual Language Support**: Returns predictions in both Thai and English
- **Image Hosting**: Automatically uploads images to Imgur
- **Rate Limiting**: Built-in protection (3 requests per IP per minute)
- **Result Storage**: MongoDB integration for storing predictions
- **RESTful API**: Simple HTTP endpoints for easy integration
- **Cloud-Ready**: Configured for Vercel deployment

## Tech Stack

- **Backend**: Flask 2.0.0
- **Machine Learning**: TensorFlow 2.11.0, Keras 2.11.0
- **Database**: MongoDB 4.3.3
- **Image Storage**: Imgur API
- **Deployment**: Vercel (serverless)

## Prerequisites

- Python 3.8 or higher
- MongoDB instance (local or cloud)
- Imgur API credentials
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/PlaiPunlawat/thai-food-image-classification-api.git
cd thai-food-image-classification-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
# Install package in development mode (for src imports)
pip install -e .
```

### 4. Configure environment variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
IMGUR_CLIENT_ID=your_imgur_client_id_here
MONGO_URI=mongodb://localhost:27017/
MONGO_DATABASE=thai_food_api
```

#### Getting Imgur API Credentials

1. Go to [Imgur API](https://api.imgur.com/oauth2/addclient)
2. Register your application
3. Copy the Client ID

#### MongoDB Setup

**Option A: Local MongoDB**
```bash
# Install MongoDB locally
# macOS
brew install mongodb-community

# Ubuntu
sudo apt-get install mongodb

# Start MongoDB
mongod
```

**Option B: MongoDB Atlas (Cloud)**
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Get connection string (replace `<password>` with your password)
4. Use in `MONGO_URI`

### 5. Run the application

```bash
python index.py
```

The API will be available at `http://localhost:5000`

## API Documentation

### Upload and Classify Image

Upload an image file and get Thai food predictions.

**Endpoint**: `POST /api/upload`

**Request**:
- Method: `POST`
- Content-Type: `multipart/form-data`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image | File | Yes | Image file (max 5MB) |
| model | String | No | Model to use: `mobilenet` or `xception` (default: `xception`) |

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "image=@/path/to/food_image.jpg" \
  -F "model=xception"
```

**Success Response** (201 Created):
```json
{
  "resultId": "507f1f77bcf86cd799439011",
  "predict_result": [
    {
      "name_en": "Pad Thai",
      "name_th": "ผัดไทย",
      "percent": "95.23"
    },
    {
      "name_en": "Pad See Ew",
      "name_th": "ผัดซีอิ๊ว",
      "percent": "2.15"
    },
    {
      "name_en": "Drunken Noodles",
      "name_th": "ผัดขี้เมา",
      "percent": "1.42"
    },
    {
      "name_en": "Fried Rice",
      "name_th": "ข้าวผัด",
      "percent": "0.89"
    },
    {
      "name_en": "Tom Yum",
      "name_th": "ต้มยำ",
      "percent": "0.31"
    }
  ],
  "status": "success",
  "message": "uploaded successfully"
}
```

**Error Responses**:

- `400 Bad Request`: Missing image file or invalid request
- `429 Too Many Requests`: Rate limit exceeded (3 requests per minute per IP)
- `413 Payload Too Large`: Image exceeds 5MB

### Get Result by ID

Retrieve previously stored prediction results.

**Endpoint**: `GET /api/result/<resultId>`

**Example Request**:
```bash
curl http://localhost:5000/api/result/507f1f77bcf86cd799439011
```

**Success Response** (200 OK):
```json
{
  "status": "success",
  "predict_result": [
    {
      "name_en": "Pad Thai",
      "name_th": "ผัดไทย",
      "percent": "95.23"
    }
  ],
  "image_url": "https://i.imgur.com/abc123.jpg"
}
```

**Error Response**:
- `404 Not Found`: Result ID does not exist

## Supported Thai Dishes

The API can classify 75 different Thai dishes including:

- Pad Thai (ผัดไทย)
- Tom Yum Goong (ต้มยำกุ้ง)
- Green Curry (แกงเขียวหวาน)
- Massaman Curry (แกงมัสมั่น)
- Som Tam (ส้มตำ)
- And 70 more...

See `foodnames.py` for the complete list.

## Model Information

### MobileNet
- **Size**: ~17 MB
- **Speed**: Faster inference
- **Use case**: Production environments requiring quick responses

### Xception
- **Size**: ~88 MB
- **Speed**: Slower but more accurate
- **Use case**: When accuracy is more important than speed

## Deployment

### Deploy to Vercel

The project is pre-configured for Vercel deployment:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

Configuration is in `vercel.json`.

### Environment Variables on Vercel

Add these environment variables in your Vercel project settings:
- `IMGUR_CLIENT_ID`
- `MONGO_URI`
- `MONGO_DATABASE`

## Development

### Project Structure

```
thai-food-image-classification-api/
├── index.py              # Flask application and API routes
├── predict.py            # Image classification logic
├── foodnames.py          # Thai food names database
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment config
├── .env.example         # Environment template
└── models/
    ├── MobileNet.h5     # MobileNet model weights
    └── Xception.h5      # Xception model weights
```

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with debug enabled (local only)
python index.py
```

## Rate Limiting

To prevent abuse, the API implements rate limiting:
- **Limit**: 3 requests per IP address per minute
- **Storage**: Tracked in MongoDB
- **Response**: HTTP 429 when limit exceeded

## Security Considerations

- Maximum upload size: 5 MB
- File type validation recommended (not currently implemented)
- Rate limiting prevents abuse
- Environment variables protect sensitive credentials
- CORS enabled for cross-origin requests

## Troubleshooting

### Common Issues

**Issue**: MongoDB connection error
```
Solution: Ensure MongoDB is running and MONGO_URI is correct
```

**Issue**: Imgur upload fails
```
Solution: Check IMGUR_CLIENT_ID is valid
```

**Issue**: Model not found error
```
Solution: Ensure .h5 model files exist in models/ directory
```

**Issue**: Memory error during prediction
```
Solution: Try using MobileNet instead of Xception (smaller model)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is available for educational and personal use.

## Acknowledgments

- TensorFlow and Keras teams for the deep learning frameworks
- Pre-trained model architectures: MobileNet and Xception
- Imgur for image hosting API
- MongoDB for data storage

## Contact

For questions or issues, please open an issue on GitHub.

---

**Note**: This API is designed for educational purposes. For production use, consider implementing additional security measures, authentication, and comprehensive error handling.
