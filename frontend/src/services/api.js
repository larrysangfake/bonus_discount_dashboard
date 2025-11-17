/**
 * API service for communicating with the backend.
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch all discounts with optional filters
 */
export const getDiscounts = async (filters = {}) => {
  try {
    const response = await api.get('/discounts', { params: filters });
    return response.data;
  } catch (error) {
    console.error('Error fetching discounts:', error);
    throw error;
  }
};

/**
 * Fetch a specific discount by ID
 */
export const getDiscount = async (id) => {
  try {
    const response = await api.get(`/discounts/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching discount:', error);
    throw error;
  }
};

/**
 * Fetch list of all supermarkets
 */
export const getSupermarkets = async () => {
  try {
    const response = await api.get('/supermarkets');
    return response.data.supermarkets;
  } catch (error) {
    console.error('Error fetching supermarkets:', error);
    throw error;
  }
};

/**
 * Fetch list of all categories
 */
export const getCategories = async () => {
  try {
    const response = await api.get('/categories');
    return response.data.categories;
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
};

/**
 * Fetch statistics
 */
export const getStats = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export default api;
