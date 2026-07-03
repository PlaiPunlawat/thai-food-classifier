"""Unit tests for PredictionService."""
import pytest
import tempfile
import os
import numpy as np
from unittest.mock import patch, MagicMock
from PIL import Image


@pytest.mark.unit
class TestPredictionService:
    """Tests for the PredictionService class."""

    def _create_test_image(self):
        """Create a temporary test image and return its path."""
        img = Image.new('RGB', (128, 128), color='red')
        fd, path = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        img.save(path)
        return path

    def _make_fake_model(self, top_index=0):
        """Create a fake model returning a fixed 72-class probability vector."""
        mock_model = MagicMock()
        predictions = np.zeros((1, 72))
        predictions[0, top_index] = 0.95
        predictions[0, (top_index + 1) % 72] = 0.02
        predictions[0, (top_index + 2) % 72] = 0.015
        predictions[0, (top_index + 3) % 72] = 0.01
        predictions[0, (top_index + 4) % 72] = 0.005
        mock_model.predict.return_value = predictions
        return mock_model

    def test_returns_top_k_sorted_descending(self):
        """Test that predict_image returns exactly top_k items sorted by percent desc."""
        from src.services.prediction_service import PredictionService

        service = PredictionService()
        fake_model = self._make_fake_model(top_index=10)
        image_path = self._create_test_image()

        try:
            with patch.object(service, '_load_model', return_value=fake_model):
                results = service.predict_image(image_path, model_name='xception', top_k=5)

            assert len(results) == 5
            percentages = [r['percent'] for r in results]
            assert percentages == sorted(percentages, reverse=True)
        finally:
            os.unlink(image_path)

    def test_result_contract_keys_and_types(self):
        """Test that each result item has correct keys and types."""
        from src.services.prediction_service import PredictionService

        service = PredictionService()
        fake_model = self._make_fake_model(top_index=5)
        image_path = self._create_test_image()

        try:
            with patch.object(service, '_load_model', return_value=fake_model):
                results = service.predict_image(image_path, model_name='mobilenet', top_k=5)

            for item in results:
                assert 'name_en' in item
                assert 'name_th' in item
                assert 'percent' in item
                assert isinstance(item['name_en'], str)
                assert isinstance(item['name_th'], str)
                assert isinstance(item['percent'], float)
                assert 0 <= item['percent'] <= 100
        finally:
            os.unlink(image_path)

    def test_percent_has_two_decimal_places(self):
        """Test that percent values are rounded to 2 decimal places."""
        from src.services.prediction_service import PredictionService

        service = PredictionService()
        mock_model = MagicMock()
        predictions = np.zeros((1, 72))
        predictions[0, 0] = 0.953456789
        mock_model.predict.return_value = predictions
        image_path = self._create_test_image()

        try:
            with patch.object(service, '_load_model', return_value=mock_model):
                results = service.predict_image(image_path, top_k=1)

            percent_str = f"{results[0]['percent']:.10f}"
            assert results[0]['percent'] == round(results[0]['percent'], 2)
        finally:
            os.unlink(image_path)

    def test_invalid_model_name_falls_back(self):
        """Test that an invalid model_name doesn't raise before prediction."""
        from src.services.prediction_service import PredictionService

        service = PredictionService()
        fake_model = self._make_fake_model(top_index=0)
        image_path = self._create_test_image()

        try:
            with patch.object(service, '_load_model', return_value=fake_model):
                results = service.predict_image(image_path, model_name='nonexistent', top_k=5)

            assert len(results) == 5
        finally:
            os.unlink(image_path)

    def test_preprocessing_pipeline_double_scaling(self):
        """
        PREPROCESSING GUARD: Verify the array passed to model.predict has values
        in [-1/255, 1/255] — i.e. preprocess_input (maps to [-1,1]) followed by /255.

        This pins the original 2022 training pipeline (see KNOWN_ISSUES.md, D5).
        If this test fails after a "cleanup" of the scaling, the cleanup is the bug.
        """
        from src.services.prediction_service import PredictionService

        service = PredictionService()
        mock_model = MagicMock()
        predictions = np.zeros((1, 72))
        predictions[0, 0] = 0.9
        mock_model.predict.return_value = predictions

        image_path = self._create_test_image()

        try:
            with patch.object(service, '_load_model', return_value=mock_model):
                service.predict_image(image_path, model_name='xception', top_k=1)

            call_args = mock_model.predict.call_args
            input_array = call_args[0][0]

            assert input_array.shape == (1, 128, 128, 3)
            # preprocess_input maps [0,255] → [-1,1], then /255 maps to [-1/255, 1/255]
            assert input_array.min() >= -1.0 / 255.0 - 1e-7
            assert input_array.max() <= 1.0 / 255.0 + 1e-7
            # Confirm values are NOT in [0,1] (plain /255) or [-1,1] (preprocess_input only)
            assert input_array.max() < 0.01, (
                "Values too large — looks like only /255 or only preprocess_input was applied"
            )
        finally:
            os.unlink(image_path)

    def test_custom_top_k(self):
        """Test that top_k parameter controls number of results."""
        from src.services.prediction_service import PredictionService

        service = PredictionService()
        mock_model = MagicMock()
        predictions = np.random.rand(1, 72)
        predictions = predictions / predictions.sum()
        mock_model.predict.return_value = predictions
        image_path = self._create_test_image()

        try:
            with patch.object(service, '_load_model', return_value=mock_model):
                results = service.predict_image(image_path, top_k=3)

            assert len(results) == 3
        finally:
            os.unlink(image_path)
