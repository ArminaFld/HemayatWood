import React from 'react';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  return (
    <div className="home-page">
      <div className="home-card">
        <h1>به حمایت چوب خوش آمدید</h1>
        <p>
          شما با موفقیت وارد شده‌اید. این صفحه فقط وقتی قابل دسترسی است
          که کاربر توکن معتبر داشته باشد.
        </p>

        <div className="home-actions">
          <button
            onClick={() => alert('اینجا بعداً می‌تونه لیست سفارش‌ها یا محصولات باشد')}
          >
            مشاهده محصولات / سفارش‌ها
          </button>

          <button className="logout-btn" onClick={handleLogout}>
            خروج از حساب
          </button>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
