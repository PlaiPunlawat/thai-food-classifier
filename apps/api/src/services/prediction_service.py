"""Image prediction service using ML models."""
import os
import numpy as np
from keras.models import load_model
from keras.preprocessing import image as keras_image
from food_labels import FOOD_LABELS as food_names
from src.config.settings import Config
from src.utils.logger import logger


class PredictionService:
    """Service for handling image predictions."""

    def __init__(self):
        """Initialize prediction service."""
        self.models = {}
        self.image_size = Config.IMAGE_SIZE

    def _load_model(self, model_name='xception'):
        """
        Load ML model from disk (cached).

        Args:
            model_name: Model to load ('xception' or 'mobilenet')

        Returns:
            Loaded Keras model
        """
        if model_name in self.models:
            return self.models[model_name]

        if model_name == 'mobilenet':
            model_path = Config.MOBILENET_MODEL
        else:
            model_path = Config.XCEPTION_MODEL

        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            raise FileNotFoundError(f"Model file not found: {model_path}")

        logger.info(f"Loading model: {model_name} from {model_path}")
        model = load_model(model_path)
        self.models[model_name] = model

        return model

    def predict_image(self, image_path, model_name='xception', top_k=5):
        """
        Predict Thai food dish from image.

        Args:
            image_path: Path to image file
            model_name: Model to use ('xception' or 'mobilenet')
            top_k: Number of top predictions to return

        Returns:
            List of top K predictions with names and confidence scores
        """
        try:
            # Load and preprocess image
            img = keras_image.load_img(image_path, target_size=self.image_size)
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # Normalize

            # Load model and predict
            model = self._load_model(model_name)
            predictions = model.predict(img_array, verbose=0)

            # Get top K predictions
            top_indices = np.argsort(predictions[0])[::-1][:top_k]

            results = []
            for idx in top_indices:
                confidence = float(predictions[0][idx]) * 100
                result = {
                    'name_en': food_names[idx]['name_en'],
                    'name_th': food_names[idx]['name_th'],
                    'percent': f'{confidence:.2f}'
                }
                results.append(result)

            logger.info(
                f"Prediction successful: {results[0]['name_en']} "
                f"({results[0]['percent']}%) using {model_name}"
            )

            return results

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise


# Create singleton instance
prediction_service = PredictionService()
