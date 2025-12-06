import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/client';
import logo from '../assets/hemayat-logo.png.png';

function VerifyPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const emailFromState = location.state?.email || '';
  const [email, setEmail] = useState(emailFromState);
  const [code, setCode] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const res = await api.post('/verify-email', { email, code });
      setMessage(res.data.message || 'تأیید انجام شد');

      if (res.data.token) {
        localStorage.setItem('accessToken', res.data.token);
        navigate('/home');
      }
    } catch (err) {
      setMessage(err.response?.data?.message || 'خطا در تأیید');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        {/* 👇 لوگو بالای فرم */}
        <img src={logo} alt="Hemayat Wood Logo" className="auth-logo" />

        <h1>تأیید حساب</h1>

        <form onSubmit={handleSubmit}>
          <input
            placeholder="ایمیل"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            placeholder="کد تأیید"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <button type="submit" disabled={loading}>
            {loading ? '...' : 'تأیید'}
          </button>
        </form>

        {message && <p className="auth-message">{message}</p>}
      </div>
    </div>
  );
}

export default VerifyPage;
