import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const login = (username, password) => api.post('/login/', { username, password });
export const register = (username, password, role) => api.post('/register/', { username, password, role });
export const createCredential = (data) => api.post('/credentials/', data);
export const verifyCredential = (id) => api.post(`/credentials/${id}/verify/`);
export const getCredentials = () => api.get('/credentials/');

export default api;