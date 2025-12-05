import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = e => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const res = await api.post('/login', form);
      localStorage.setItem('accessToken', res.data.token);
      setMessage('ورود موفق بود');
      navigate('/home');
    } catch (err) {
      setMessage(err.response?.data?.message || 'خطا در ورود');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
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
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default LoginPage;
