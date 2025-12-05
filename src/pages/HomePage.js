import React from 'react';

function HomePage() {
  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    window.location.href = '/login';
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>خوش آمدید 🌿</h2>
      <p>شما وارد سیستم شده‌اید.</p>

      <button onClick={handleLogout}>خروج از حساب</button>
    </div>
  );
}

export default HomePage;
