/**
 * Application-wide constants
 */

// Theme colors
export const COLORS = {
  primary: '#987737',
  dark: '#222',
  black: '#121212',
};

// File upload constraints
export const UPLOAD_CONSTRAINTS = {
  maxFileSize: 5 * 1024 * 1024, // 5MB in bytes
  acceptedFormats: ['.png', '.jpg', '.jpeg'],
  acceptedMimeTypes: ['image/png', 'image/jpeg', 'image/jpg'],
};

// ML Models
export const ML_MODELS = {
  XCEPTION: 'xception',
  MOBILENET: 'mobilenet',
};

// API endpoints
export const API_ENDPOINTS = {
  upload: '/upload',
  result: '/result',
};
