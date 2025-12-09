import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import logo from '../assets/hemayat-logo.png.png';

function RegisterPage() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
  });
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
      // بک‌اند ما برای ثبت نام این سه فیلد را می‌خواهد
      const payload = {
        username: form.username,
        email: form.email,
        password: form.password,
      };

      const res = await api.post('/api/auth/register', payload);

      setMessage(
        res.data.message ||
        'ثبت نام انجام شد. لطفاً کد تأیید ۶ رقمی را وارد کنید.'
      );

      // ایمیل را برای صفحه وریفای می‌فرستیم
      navigate('/verify', { state: { email: form.email } });
    } catch (err) {
      const backendMsg =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'خطا در ثبت نام';
      setMessage(backendMsg);
      console.error('Register error:', err);
    } finally {
      setLoading(false);
    }
  };

  const goToLogin = () => {
    navigate('/login');
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <img src={logo} alt="Hemayat Wood Logo" className="auth-logo" />
        <h1>ثبت نام</h1>

        <form onSubmit={handleSubmit}>
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

          <button
            type="button"
            className="auth-secondary-button"
            onClick={goToLogin}
          >
            آیا قبلاً ثبت‌نام کرده‌اید؟ ورود
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default RegisterPage;
