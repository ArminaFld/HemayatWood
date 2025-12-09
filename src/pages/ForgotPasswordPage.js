// src/pages/ForgotPasswordPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import logo from '../assets/hemayat-logo.png.png';

function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const res = await api.post('/api/auth/forgot-password', { email });

      // اگر سرور پیامی برگرداند همان را نشان می‌دهیم، وگرنه پیام پیش‌فرض
      setMessage(res.data.message || 'کد بازیابی برای شما ارسال شد.');

      // بعد از موفقیت، کاربر را به صفحه‌ی تنظیم رمز جدید می‌بریم
      navigate('/reset-password', { state: { email } });
    } catch (err) {
      setMessage(
        err.response?.data?.detail || 'خطا در ارسال کد بازیابی رمز عبور'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <img src={logo} alt="Hemayat Wood Logo" className="auth-logo" />
        <h1>فراموشی رمز عبور</h1>

        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="ایمیل"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button type="submit" disabled={loading}>
            {loading ? '...' : 'ارسال کد بازیابی'}
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default ForgotPasswordPage;
