"""Unit tests for prediction logic."""
import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
import numpy as np


@pytest.mark.unit
class TestPredictImage:
    """Tests for predict_image function."""

    def test_predict_image_with_xception(self):
        """Test image prediction using Xception model."""
        from predict import predict_image

        # Create a temporary test image
        from PIL import Image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            img = Image.new('RGB', (128, 128), color='red')
            img.save(f.name)
            temp_path = f.name

        try:
            # Mock the model loading and prediction
            with patch('predict.load_model') as mock_load:
                mock_model = MagicMock()
                # Mock prediction to return probabilities for 75 classes
                mock_predictions = np.zeros((1, 72))
                mock_predictions[0, 0] = 0.95  # Highest probability for first class
                mock_predictions[0, 1] = 0.02
                mock_predictions[0, 2] = 0.01
                mock_predictions[0, 3] = 0.01
                mock_predictions[0, 4] = 0.01

                mock_model.predict.return_value = mock_predictions
                mock_load.return_value = mock_model

                result = predict_image(temp_path, model='xception')

                # Verify result structure
                assert isinstance(result, list)
                assert len(result) == 5  # Top 5 predictions
                assert 'name_en' in result[0]
                assert 'name_th' in result[0]
                assert 'percent' in result[0]

                # Verify model was loaded correctly
                mock_load.assert_called_once()
                assert 'Xception.h5' in str(mock_load.call_args)

        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_predict_image_with_mobilenet(self):
        """Test image prediction using MobileNet model."""
        from predict import predict_image

        # Create a temporary test image
        from PIL import Image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            img = Image.new('RGB', (128, 128), color='blue')
            img.save(f.name)
            temp_path = f.name

        try:
            with patch('predict.load_model') as mock_load:
                mock_model = MagicMock()
                mock_predictions = np.zeros((1, 72))
                mock_predictions[0, 10] = 0.85

                mock_model.predict.return_value = mock_predictions
                mock_load.return_value = mock_model

                result = predict_image(temp_path, model='mobilenet')

                # Verify MobileNet model was loaded
                mock_load.assert_called_once()
                assert 'MobileNet.h5' in str(mock_load.call_args)

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_predict_image_returns_top_5(self):
        """Test that prediction returns exactly 5 results."""
        from predict import predict_image

        from PIL import Image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            img = Image.new('RGB', (128, 128), color='green')
            img.save(f.name)
            temp_path = f.name

        try:
            with patch('predict.load_model') as mock_load:
                mock_model = MagicMock()
                # Create random predictions for all 75 classes
                mock_predictions = np.random.rand(1, 72)
                mock_predictions = mock_predictions / mock_predictions.sum()  # Normalize

                mock_model.predict.return_value = mock_predictions
                mock_load.return_value = mock_model

                result = predict_image(temp_path, model='xception')

                # Should return exactly top 5 predictions
                assert len(result) == 5

                # Percentages should be in descending order
                percentages = [float(r['percent']) for r in result]
                assert percentages == sorted(percentages, reverse=True)

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_predict_image_percentage_format(self):
        """Test that percentages are formatted correctly."""
        from predict import predict_image

        from PIL import Image
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            img = Image.new('RGB', (128, 128), color='yellow')
            img.save(f.name)
            temp_path = f.name

        try:
            with patch('predict.load_model') as mock_load:
                mock_model = MagicMock()
                mock_predictions = np.zeros((1, 72))
                mock_predictions[0, 0] = 0.95234
                mock_predictions[0, 1] = 0.02156

                mock_model.predict.return_value = mock_predictions
                mock_load.return_value = mock_model

                result = predict_image(temp_path, model='xception')

                # Check percentage format (should be string with 2 decimal places)
                assert isinstance(result[0]['percent'], str)
                # Should have format like "95.23"
                assert '.' in result[0]['percent']

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


@pytest.mark.unit
class TestFoodNames:
    """Tests for food names data."""

    def test_food_names_structure(self):
        """Test that food names are properly structured."""
        from food_labels import FOOD_LABELS as food_names

        assert isinstance(food_names, list)
        assert len(food_names) == 72

        # Check structure of each entry
        for food in food_names:
            assert isinstance(food, dict)
            assert 'name_en' in food
            assert 'name_th' in food
            assert isinstance(food['name_en'], str)
            assert isinstance(food['name_th'], str)
            assert len(food['name_en']) > 0
            assert len(food['name_th']) > 0

    def test_food_names_uniqueness(self):
        """Test that food names are unique."""
        from food_labels import FOOD_LABELS as food_names

        english_names = [f['name_en'] for f in food_names]
        thai_names = [f['name_th'] for f in food_names]

        # All English names should be unique
        assert len(english_names) == len(set(english_names))
        # All Thai names should be unique
        assert len(thai_names) == len(set(thai_names))
