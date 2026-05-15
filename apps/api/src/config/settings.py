"""Application configuration and settings."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'thai_food_api')

    # Imgur
    IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')

    # Rate Limiting
    RATE_LIMIT_REQUESTS = 3
    RATE_LIMIT_WINDOW_MINUTES = 1

    # Models
    HF_MODEL_REPO = os.getenv('HF_MODEL_REPO', 'PlaiPunlawat/thai-food-classifier')
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models'))
    DEFAULT_MODEL = 'xception'

    # Image Processing
    IMAGE_SIZE = (128, 128)


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = False  # Changed from True for security
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    MONGO_DATABASE = 'thai_food_api_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment."""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
