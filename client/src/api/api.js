import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const login = (username, password) => api.post('/users/login/', { username, password });
export const register = (username, password, role) => api.post('/register/', { username, password, role });
export const createCredential = (data) => api.post('/credentials/', data);
export const verifyCredential = (id) => api.post(`/credentials/${id}/verify/`);
export const getCredentials = () => api.get('/credentials/');
export const getWalletBalance = () => api.get('/wallet/balance/');
export const generateWalletAddress = () => api.post('/wallet/generate/');

export default api;