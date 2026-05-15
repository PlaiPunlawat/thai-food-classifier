"""Pytest configuration and fixtures."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "packages" / "shared"))

import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch
from index import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test Flask app instance."""
    flask_app.config.update({
        'TESTING': True,
        'UPLOAD_FOLDER': tempfile.gettempdir(),
        'MAX_CONTENT_LENGTH': 5 * 1024 * 1024,
    })
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def mock_mongo():
    """Mock MongoDB client."""
    with patch('index.get_mongo_client') as mock:
        mock_db = MagicMock()
        mock_db['requests'].count_documents.return_value = 0
        mock_db['requests'].insert_one.return_value = None
        mock_db['results'].insert_one.return_value = MagicMock(inserted_id='507f1f77bcf86cd799439011')
        mock_db['results'].find_one.return_value = {
            '_id': '507f1f77bcf86cd799439011',
            'image_url': 'https://i.imgur.com/test.jpg',
            'predict_result': [
                {'name_en': 'Pad Thai', 'name_th': 'ผัดไทย', 'percent': '95.23'}
            ]
        }
        mock.return_value = mock_db
        yield mock_db


@pytest.fixture
def mock_imgur():
    """Mock Imgur API response."""
    with patch('requests.post') as mock:
        mock.return_value.json.return_value = {
            'data': {'link': 'https://i.imgur.com/test.jpg'}
        }
        yield mock


@pytest.fixture
def mock_predict():
    """Mock predict_image function."""
    with patch('index.predict_image') as mock:
        mock.return_value = [
            {'name_en': 'Pad Thai', 'name_th': 'ผัดไทย', 'percent': '95.23'},
            {'name_en': 'Pad See Ew', 'name_th': 'ผัดซีอิ๊ว', 'percent': '2.15'},
            {'name_en': 'Drunken Noodles', 'name_th': 'ผัดขี้เมา', 'percent': '1.42'},
            {'name_en': 'Fried Rice', 'name_th': 'ข้าวผัด', 'percent': '0.89'},
            {'name_en': 'Tom Yum', 'name_th': 'ต้มยำ', 'percent': '0.31'}
        ]
        yield mock


@pytest.fixture
def sample_image():
    """Create a sample image file for testing."""
    # Create a minimal valid image file
    from PIL import Image
    import io

    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv('IMGUR_CLIENT_ID', 'test_imgur_client_id')
    monkeypatch.setenv('MONGO_URI', 'mongodb://localhost:27017/')
    monkeypatch.setenv('MONGO_DATABASE', 'test_db')
