import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import logo from '../assets/hemayat-logo.png.png';

function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      // این مسیر را بر اساس swagger گیت‌وی تنظیم کردیم
      const res = await api.post('/api/auth/login', form);

      // هم access_token را چک می‌کنیم هم token
      const token = res.data.access_token || res.data.token;

      if (token) {
        localStorage.setItem('accessToken', token);
        setMessage('ورود موفق بود');
        navigate('/home');
      } else {
        setMessage('توکن از سرور دریافت نشد');
      }
    } catch (err) {
      setMessage(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'خطا در ورود'
      );
    } finally {
      setLoading(false);
    }
  };

  const goToForgotPassword = () => {
    navigate('/verify');
  };

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
            {loading ? '...' : 'ورود'}
          </button>

          <button
            type="button"
            className="auth-secondary-button"
            onClick={goToForgotPassword}
          >
            آیا رمز عبور خود را فراموش کرده‌اید؟
          </button>

          <button
            type="button"
            className="auth-secondary-button"
            onClick={goToRegister}
          >
            آیا هنوز ثبت‌نام نکرده‌اید؟ ثبت‌نام
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default LoginPage;
