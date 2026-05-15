import axios from 'axios';

/**
 * Configure axios instance with base URL from environment
 */
export const configureApi = () => {
  if (process.env.NEXT_PUBLIC_API_ENDPOINT) {
    axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_ENDPOINT;
  }
};

/**
 * API client instance
 * Use this for all API calls instead of axios directly
 */
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_ENDPOINT,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload image for prediction
 * @param {File} file - Image file to upload
 * @param {string} model - ML model to use (xception or mobilenet)
 * @param {Function} onProgress - Progress callback
 * @returns {Promise} API response with prediction results
 */
export const uploadImage = async (file, model = 'xception', onProgress) => {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('model', model);

  return apiClient.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: onProgress,
  });
};

/**
 * Get prediction result by ID
 * @param {string} resultId - Result ID to fetch
 * @returns {Promise} API response with result data
 */
export const getResult = async (resultId) => {
  return apiClient.get(`/result/${resultId}`);
};
