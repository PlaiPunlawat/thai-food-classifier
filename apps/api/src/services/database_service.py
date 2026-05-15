"""Database service for MongoDB operations."""
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from src.config.settings import Config
from src.utils.logger import logger


class DatabaseService:
    """Service for handling database operations."""

    def __init__(self):
        """Initialize database service."""
        self.client = None
        self.db = None

    def get_database(self):
        """
        Get MongoDB database connection.

        Returns:
            MongoDB database instance
        """
        if self.db is None:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.MONGO_DATABASE]
            logger.info(f"Connected to MongoDB: {Config.MONGO_DATABASE}")
        return self.db

    def check_rate_limit(self, ip_address):
        """
        Check if IP address has exceeded rate limit.

        Args:
            ip_address: IP address to check

        Returns:
            bool: True if rate limit exceeded, False otherwise
        """
        db = self.get_database()

        now = datetime.datetime.now()
        window_start = now - datetime.timedelta(minutes=Config.RATE_LIMIT_WINDOW_MINUTES)

        count = db['requests'].count_documents({
            'ip': ip_address,
            'timestamp': {'$gte': window_start}
        })

        exceeded = count >= Config.RATE_LIMIT_REQUESTS

        if exceeded:
            logger.warning(f"Rate limit exceeded for IP: {ip_address} ({count} requests)")

        return exceeded

    def log_request(self, ip_address):
        """
        Log a request for rate limiting.

        Args:
            ip_address: IP address making the request
        """
        db = self.get_database()
        db['requests'].insert_one({
            'ip': ip_address,
            'timestamp': datetime.datetime.now()
        })

    def save_result(self, image_url, predict_result):
        """
        Save prediction result to database.

        Args:
            image_url: URL of the uploaded image
            predict_result: Prediction results

        Returns:
            str: Inserted document ID
        """
        db = self.get_database()

        result = db['results'].insert_one({
            'image_url': image_url,
            'predict_result': predict_result,
            'created_at': datetime.datetime.now()
        })

        result_id = str(result.inserted_id)
        logger.info(f"Saved prediction result: {result_id}")

        return result_id

    def get_result(self, result_id):
        """
        Retrieve prediction result by ID.

        Args:
            result_id: Result document ID

        Returns:
            dict: Result document or None if not found
        """
        db = self.get_database()

        try:
            result = db['results'].find_one({'_id': ObjectId(result_id)})
            if result:
                logger.info(f"Retrieved result: {result_id}")
            else:
                logger.warning(f"Result not found: {result_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to retrieve result {result_id}: {str(e)}")
            return None


# Create singleton instance
database_service = DatabaseService()
