// src/pages/ResetPasswordPage.js
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/client';
import logo from '../assets/hemayat-logo.png.png';

function ResetPasswordPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // اگر از صفحه قبل ایمیل ارسال شده بود، از همان استفاده می‌کنیم
  const emailFromState = location.state?.email || '';
  const [email, setEmail] = useState(emailFromState);
  const [code, setCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const res = await api.post('/api/auth/reset-password', {
        email,
        code,
        new_password: newPassword,
      });

      setMessage(res.data.message || 'رمز عبور با موفقیت تغییر کرد.');

      // بعد از موفقیت، کاربر را به صفحه‌ی لاگین می‌بریم
      navigate('/login');
    } catch (err) {
      setMessage(
        err.response?.data?.detail || 'خطا در تغییر رمز عبور'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <img src={logo} alt="Hemayat Wood Logo" className="auth-logo" />
        <h1>تنظیم رمز جدید</h1>

        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="ایمیل"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            placeholder="کد ۶ رقمی"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />

          <input
            type="password"
            placeholder="رمز عبور جدید"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />

          <button type="submit" disabled={loading}>
            {loading ? '...' : 'تأیید و تغییر رمز'}
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default ResetPasswordPage;
