"""Thai Food Image Classification API - Main Application."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "packages" / "shared"))

from flask import Flask
import tempfile
from flask_cors import CORS, cross_origin
from src.config.settings import get_config
from src.utils.logger import setup_logger
from src.api.routes import upload_image as upload_handler, get_result as get_result_handler

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config = get_config()
app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['CORS_HEADERS'] = 'Content-Type'

# Enable CORS
cors = CORS(app)

# Setup logging
logger = setup_logger('thai_food_api')


@app.post('/api/upload')
@cross_origin()
def upload_image():
    """Handle image upload and prediction."""
    return upload_handler()


@app.get('/api/result/<resultId>')
@cross_origin()
def get_result(resultId):
    """Retrieve prediction result by ID."""
    return get_result_handler(resultId)


@app.get('/health')
def health_check():
    """Health check endpoint."""
    return {'status': 'healthy', 'service': 'Thai Food Classification API'}, 200


if __name__ == "__main__":
    # For local development only - never run with debug=True in production
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    logger.info(f"Starting application in {'DEBUG' if debug_mode else 'PRODUCTION'} mode")
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
