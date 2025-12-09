// src/pages/LoginPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import logo from '../assets/hemayat-logo.png.png';

function LoginPage() {
  const [form, setForm] = useState({
    username: '',
    password: '',
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const res = await api.post('/api/auth/login', form);
      localStorage.setItem('accessToken', res.data.access_token);
      setMessage('ورود موفق بود');
      navigate('/home');
    } catch (err) {
      setMessage(err.response?.data?.detail || 'خطا در ورود');
    } finally {
      setLoading(false);
    }
  };

  // 👉 رفتن به صفحه فراموشی رمز
  const goToForgotPassword = () => {
    navigate('/forgot-password');
  };

  // 👉 رفتن به صفحه ثبت‌نام
  const goToRegister = () => {
    navigate('/register');
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <img src={logo} alt="Hemayat Wood Logo" className="auth-logo" />

        <h1>ورود</h1>

        <form onSubmit={handleSubmit}>
          <input
            name="username"
            placeholder="نام کاربری"
            value={form.username}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            placeholder="رمز عبور"
            value={form.password}
            onChange={handleChange}
          />

          {/* دکمه اصلی ورود */}
          <button type="submit" disabled={loading}>
            {loading ? '...' : 'ورود'}
          </button>

          {/* 👇 دکمه فراموشی رمز – حتماً type="button" باشد */}
          <button
            type="button"
            className="auth-secondary-button"
            onClick={goToForgotPassword}
          >
            آیا رمز عبور خود را فراموش کرده‌اید؟
          </button>

          {/* 👇 دکمه رفتن به ثبت‌نام */}
          <button
            type="button"
            className="auth-secondary-button"
            onClick={goToRegister}
          >
            هنوز ثبت‌نام نکرده‌اید؟ ثبت‌نام
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default LoginPage;
