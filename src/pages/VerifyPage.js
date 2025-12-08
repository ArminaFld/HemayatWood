import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/client';
import logo from '../assets/hemayat-logo.png.png';

function VerifyPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // اگر از صفحه ثبت‌نام ایمیل فرستاده شده بود، همونو بگیر
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
      // درخواست تأیید به Gateway
      const res = await api.post('/api/auth/verify', { email, code });

      // پیام موفقیت از سرور
      setMessage(res.data.message || 'حساب شما تأیید شد');

      // بعد از کمی مکث، کاربر را به صفحه لاگین ببر
      setTimeout(() => {
        navigate('/login', { replace: true });
      }, 1000);
    } catch (err) {
      // اگر خطایی از سمت سرور اومد، متن خطا رو نشون بده
      setMessage(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'خطا در تأیید'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        {/* لوگو بالای فرم */}
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
