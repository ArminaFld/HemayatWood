import axios from 'axios';

const api = axios.create({
  // آدرس API Gateway
  baseURL: 'http://localhost:9000',
});

api.interceptors.request.use(
  (config) => {
    // قبل از هر درخواست، اگر توکن در localStorage بود بفرست تو هدر
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
