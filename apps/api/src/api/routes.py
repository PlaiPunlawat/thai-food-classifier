"""API route handlers."""
import os
import uuid
import tempfile
from flask import request, jsonify
from src.services.prediction_service import prediction_service
from src.services.image_service import image_service
from src.services.database_service import database_service
from src.utils.logger import logger


def upload_image():
    """
    Handle image upload and prediction.

    Returns:
        JSON response with prediction results
    """
    # Get client IP
    ip_address = request.remote_addr

    # Check rate limit
    if database_service.check_rate_limit(ip_address):
        logger.warning(f"Rate limit exceeded for {ip_address}")
        return jsonify({'message': 'Too many requests'}), 429

    # Validate request
    if 'image' not in request.files:
        logger.warning("Upload request missing image file")
        return jsonify({'message': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        logger.warning("Upload request with empty filename")
        return jsonify({'message': 'No image file selected'}), 400

    try:
        # Log request
        database_service.log_request(ip_address)

        # Save uploaded file temporarily
        file_name = str(uuid.uuid4())
        file_path = os.path.join(tempfile.gettempdir(), file_name)
        file.save(file_path)

        logger.info(f"Processing image upload from {ip_address}")

        # Get model selection (default to xception)
        model = request.form.get('model', 'xception')

        # Predict
        predict_result = prediction_service.predict_image(file_path, model=model)

        # Upload to Imgur
        image_url = image_service.upload_to_imgur(file_path)

        # Clean up temporary file
        if os.path.exists(file_path):
            os.unlink(file_path)

        # Save result to database
        result_id = database_service.save_result(image_url, predict_result)

        logger.info(f"Upload processed successfully: {result_id}")

        return jsonify({
            'resultId': result_id,
            'predict_result': predict_result,
            'status': 'success',
            'message': 'uploaded successfully'
        }), 201

    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)

        # Clean up temporary file on error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.unlink(file_path)

        return jsonify({
            'status': 'error',
            'message': 'Failed to process image'
        }), 500


def get_result(result_id):
    """
    Retrieve prediction result by ID.

    Args:
        result_id: Result document ID

    Returns:
        JSON response with result
    """
    try:
        result = database_service.get_result(result_id)

        if result is None:
            return jsonify({'message': 'Not found'}), 404

        return jsonify({
            'status': 'success',
            'predict_result': result['predict_result'],
            'image_url': result['image_url']
        }), 200

    except Exception as e:
        logger.error(f"Failed to retrieve result: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve result'
        }), 500
