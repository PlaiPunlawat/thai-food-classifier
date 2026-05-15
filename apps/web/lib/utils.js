import { UPLOAD_CONSTRAINTS } from './constants';

/**
 * Validate file size
 * @param {File} file - File to validate
 * @returns {boolean} True if file size is within limit
 */
export const validateFileSize = (file) => {
  return file.size <= UPLOAD_CONSTRAINTS.maxFileSize;
};

/**
 * Validate file type
 * @param {File} file - File to validate
 * @returns {boolean} True if file type is accepted
 */
export const validateFileType = (file) => {
  return UPLOAD_CONSTRAINTS.acceptedMimeTypes.includes(file.type);
};

/**
 * Format file size to human-readable string
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size (e.g., "2.5 MB")
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

/**
 * Read file as data URL
 * @param {File} file - File to read
 * @returns {Promise<string>} Data URL of the file
 */
export const readFileAsDataURL = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
};
