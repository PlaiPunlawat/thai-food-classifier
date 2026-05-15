"""Unit tests for API endpoints."""
import pytest
import io
from bson.objectid import ObjectId


@pytest.mark.unit
class TestUploadEndpoint:
    """Tests for POST /api/upload endpoint."""

    def test_upload_image_success(self, client, mock_db_service, mock_imgur, mock_predict, mock_env_vars, sample_image):
        """Test successful image upload and prediction."""
        response = client.post(
            '/api/upload',
            data={
                'image': (sample_image, 'test.jpg'),
                'model': 'xception'
            },
            content_type='multipart/form-data'
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['message'] == 'uploaded successfully'
        assert 'resultId' in data
        assert 'predict_result' in data
        assert len(data['predict_result']) == 5
        assert data['predict_result'][0]['name_en'] == 'Pad Thai'

    def test_upload_image_mobilenet_model(self, client, mock_db_service, mock_imgur, mock_predict, mock_env_vars, sample_image):
        """Test upload with MobileNet model."""
        response = client.post(
            '/api/upload',
            data={
                'image': (sample_image, 'test.jpg'),
                'model': 'mobilenet'
            },
            content_type='multipart/form-data'
        )

        assert response.status_code == 201
        mock_predict.predict_image.assert_called_once()
        call_args = mock_predict.predict_image.call_args
        assert call_args[1]['model'] == 'mobilenet'

    def test_upload_missing_image(self, client, mock_db_service, mock_env_vars):
        """Test upload without image file."""
        response = client.post('/api/upload')

        assert response.status_code == 400

    def test_upload_empty_filename(self, client, mock_db_service, mock_env_vars):
        """Test upload with empty filename."""
        response = client.post(
            '/api/upload',
            data={'image': (io.BytesIO(b''), '')},
            content_type='multipart/form-data'
        )

        assert response.status_code == 400

    def test_rate_limiting(self, client, mock_env_vars):
        """Test rate limiting (3 requests per minute)."""
        from unittest.mock import patch, MagicMock

        with patch('src.api.routes.database_service') as mock:
            mock.check_rate_limit.return_value = True

            response = client.post(
                '/api/upload',
                data={'image': (io.BytesIO(b'fake image'), 'test.jpg')},
                content_type='multipart/form-data'
            )

            assert response.status_code == 429
            data = response.get_json()
            assert data['message'] == 'Too many requests'

    def test_upload_default_model(self, client, mock_db_service, mock_imgur, mock_predict, mock_env_vars, sample_image):
        """Test upload without specifying model (should default to xception)."""
        response = client.post(
            '/api/upload',
            data={'image': (sample_image, 'test.jpg')},
            content_type='multipart/form-data'
        )

        assert response.status_code == 201
        call_args = mock_predict.predict_image.call_args
        assert call_args[1]['model'] == 'xception'


@pytest.mark.unit
class TestGetResultEndpoint:
    """Tests for GET /api/result/<resultId> endpoint."""

    def test_get_result_success(self, client, mock_db_service, mock_env_vars):
        """Test successful result retrieval."""
        result_id = '507f1f77bcf86cd799439011'
        response = client.get(f'/api/result/{result_id}')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'predict_result' in data
        assert 'image_url' in data
        assert data['image_url'] == 'https://i.imgur.com/test.jpg'

    def test_get_result_not_found(self, client, mock_env_vars):
        """Test result retrieval with non-existent ID."""
        from unittest.mock import patch, MagicMock

        with patch('src.api.routes.database_service') as mock:
            mock.get_result.return_value = None

            result_id = '507f1f77bcf86cd799439011'
            response = client.get(f'/api/result/{result_id}')

            assert response.status_code == 404
            data = response.get_json()
            assert data['message'] == 'Not found'


@pytest.mark.unit
class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self, client, mock_db_service, mock_imgur, mock_predict, mock_env_vars, sample_image):
        """Test that CORS headers are present in response."""
        response = client.post(
            '/api/upload',
            data={'image': (sample_image, 'test.jpg')},
            content_type='multipart/form-data'
        )

        assert 'Access-Control-Allow-Origin' in response.headers


@pytest.mark.unit
class TestAppConfiguration:
    """Tests for Flask app configuration."""

    def test_max_content_length(self, app):
        """Test max content length is set to 5MB."""
        assert app.config['MAX_CONTENT_LENGTH'] == 5 * 1024 * 1024

    def test_upload_folder_configured(self, app):
        """Test upload folder is configured."""
        assert 'UPLOAD_FOLDER' in app.config
