"""Pytest configuration and fixtures."""
import pytest
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
def mock_db_service():
    """Mock database service."""
    with patch('src.api.routes.database_service') as mock:
        mock.check_rate_limit.return_value = False
        mock.log_request.return_value = None
        mock.save_result.return_value = '507f1f77bcf86cd799439011'
        mock.get_result.return_value = {
            '_id': '507f1f77bcf86cd799439011',
            'image_url': 'https://i.imgur.com/test.jpg',
            'predict_result': [
                {'name_en': 'Pad Thai', 'name_th': 'ผัดไทย', 'percent': '95.23'}
            ]
        }
        yield mock


@pytest.fixture
def mock_imgur():
    """Mock image service."""
    with patch('src.api.routes.image_service') as mock:
        mock.upload_to_imgur.return_value = 'https://i.imgur.com/test.jpg'
        yield mock


@pytest.fixture
def mock_predict():
    """Mock prediction service."""
    with patch('src.api.routes.prediction_service') as mock:
        mock.predict_image.return_value = [
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
