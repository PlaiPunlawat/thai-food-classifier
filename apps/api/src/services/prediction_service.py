"""Image prediction service using ML models."""
import os
import numpy as np
from keras.models import load_model
from keras.utils import load_img, img_to_array
from huggingface_hub import hf_hub_download
from src.config.food_names import food_names
from src.config.settings import Config
from src.utils.logger import logger
from keras.applications.xception import preprocess_input


class PredictionService:
    """Service for handling image predictions."""

    def __init__(self):
        """Initialize prediction service."""
        self.models = {}
        self.image_size = Config.IMAGE_SIZE

    def _load_model(self, model_name='xception'):
        """
        Load ML model from disk (cached). Downloads from HF Hub if missing.

        Args:
            model_name: Model to load ('xception' or 'mobilenet')

        Returns:
            Loaded Keras model
        """
        if model_name in self.models:
            return self.models[model_name]

        if model_name == 'mobilenet':
            model_path = Config.MOBILENET_MODEL
            hf_filename = 'MobileNet.h5'
        else:
            model_path = Config.XCEPTION_MODEL
            hf_filename = 'Xception.h5'

        if not os.path.exists(model_path):
            logger.info(
                f"Model file not found locally, downloading {hf_filename} "
                f"from {Config.HF_MODEL_REPO}..."
            )
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            hf_hub_download(
                repo_id=Config.HF_MODEL_REPO,
                filename=hf_filename,
                local_dir=Config.MODEL_PATH,
            )
            logger.info(f"Download complete: {hf_filename}")

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
            list[dict]: Top K predictions, each containing:
                - name_en (str): English dish name
                - name_th (str): Thai dish name
                - percent (float): Confidence score 0–100, rounded to 2 dp
        """
        try:
            # Load and preprocess image
            img = load_img(image_path, target_size=self.image_size)
            img_array = img_to_array(img)
            # Match the original 2022 training pipeline: preprocess_input ([-1,1])
            # followed by /255. This double-scaling looks like a bug, but the models
            # were TRAINED with it — do NOT "fix" to plain /255 or preprocess_input
            # alone, or predictions become confidently wrong. Verified 04 Jul 2026
            # (see KNOWN_ISSUES.md, D5).
            img_array = preprocess_input(img_array) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

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
                    'percent': round(confidence, 2)
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
