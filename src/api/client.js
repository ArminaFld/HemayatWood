import axios from 'axios';

// ساخت یک نمونه axios با آدرس پایه‌ی گیت‌وی / بک‌اند
const api = axios.create({
  baseURL: 'http://localhost:4000/api' // اگر بک‌اند روی پورت/آدرس دیگه بود، فقط همین رو عوض کن
});

// قبل از هر درخواست، اگر توکن داشتیم، روی هدر Authorization می‌گذاریم
api.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
