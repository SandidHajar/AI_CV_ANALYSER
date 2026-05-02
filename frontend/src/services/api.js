import axios from 'axios';

const isProd = import.meta.env.PROD;
const api = axios.create({
  baseURL: isProd ? '/api' : 'http://localhost:8000',
});

// Add a request interceptor to include the JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const loginUser = (email, password) => {
  return api.post('/auth/login', { email, password }).then(res => res.data);
};

export const registerUser = (email, password) => {
  return api.post('/auth/register', { email, password }).then(res => res.data);
};

export const uploadCV = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/extract-text', formData, {
    timeout: 30000,
  }).then(res => res.data);
};

export const analyzeCV = (text) => {
  return api.post('/analyze-cv', { cv_text: text }, {
    timeout: 30000,
  }).then(res => res.data); // Returns { job_id: "...", status: "pending" }
};

export const checkAnalysisStatus = (jobId) => {
  return api.get(`/analysis-status/${jobId}`).then(res => res.data);
};

export default api;

