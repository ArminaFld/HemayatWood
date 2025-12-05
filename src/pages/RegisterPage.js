import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

function RegisterPage() {
  const [form, setForm] = useState({
    phone: '',
    username: '',
    email: '',
    password: ''
  });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // آپدیت شدن state فرم وقتی کاربر تایپ می‌کند
  const handleChange = e => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  // ارسال فرم ثبت‌نام به بک‌اند
  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const res = await api.post('/register', form);
      setMessage(res.data.message || 'ثبت نام انجام شد');
      // بعد از ثبت‌نام، کاربر را به صفحه وارد کردن کد تأیید می‌بریم
      navigate('/verify', { state: { email: form.email } });
    } catch (err) {
      setMessage(err.response?.data?.message || 'خطا در ثبت نام');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>ثبت نام</h1>
        <form onSubmit={handleSubmit}>
          <input
            name="phone"
            placeholder="شماره همراه"
            value={form.phone}
            onChange={handleChange}
          />
          <input
            name="username"
            placeholder="نام کاربری"
            value={form.username}
            onChange={handleChange}
          />
          <input
            name="email"
            placeholder="ایمیل"
            value={form.email}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            placeholder="رمز عبور"
            value={form.password}
            onChange={handleChange}
          />
          <button type="submit" disabled={loading}>
            {loading ? '...' : 'ثبت نام'}
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default RegisterPage;
