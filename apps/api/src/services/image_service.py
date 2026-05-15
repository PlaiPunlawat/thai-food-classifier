"""Image upload and storage service."""
import requests
from src.config.settings import Config
from src.utils.logger import logger


class ImageService:
    """Service for handling image uploads to external storage."""

    def __init__(self):
        """Initialize image service."""
        self.imgur_client_id = Config.IMGUR_CLIENT_ID

    def upload_to_imgur(self, image_path):
        """
        Upload image to Imgur.

        Args:
            image_path: Path to image file

        Returns:
            str: URL of uploaded image

        Raises:
            Exception: If upload fails
        """
        try:
            with open(image_path, 'rb') as image_file:
                response = requests.post(
                    "https://api.imgur.com/3/upload",
                    files={'image': image_file},
                    headers={'Authorization': f'Client-ID {self.imgur_client_id}'},
                    timeout=30
                )

            if response.status_code == 200:
                image_url = response.json()['data']['link']
                logger.info(f"Image uploaded to Imgur: {image_url}")
                return image_url
            else:
                logger.error(f"Imgur upload failed: {response.status_code} - {response.text}")
                raise Exception(f"Imgur upload failed with status {response.status_code}")

        except Exception as e:
            logger.error(f"Failed to upload image: {str(e)}")
            raise


# Create singleton instance
image_service = ImageService()
