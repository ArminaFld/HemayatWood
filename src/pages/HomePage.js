import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

function HomePage() {
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMe = async () => {
      try {
        const res = await api.get('/api/auth/me');
        setUser(res.data);
      } catch (err) {
        setMessage(
          err.response?.data?.detail ||
          err.response?.data?.message ||
          'خطا در دریافت اطلاعات کاربر'
        );
      }
    };

    fetchMe();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  return (
    <div className="home-page">
      <div className="home-card">
        <h1>پنل کاربری حمایت‌وود</h1>

        {user ? (
          <>
            <p>خوش آمدید، {user.username} ({user.email})</p>
            <p>وضعیت تأیید حساب: {user.is_verified ? 'تأیید شده' : 'تأیید نشده'}</p>
          </>
        ) : (
          <p>در حال دریافت اطلاعات کاربر...</p>
        )}

        {message && <p className="auth-message">{message}</p>}

        <div className="home-actions">
          <button onClick={handleLogout} className="logout-btn">
            خروج
          </button>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
