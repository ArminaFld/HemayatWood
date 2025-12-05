import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import VerifyPage from './pages/VerifyPage';
import HomePage from './pages/HomePage';

// روت محافظت‌شده: اگر توکن نداشت، اجازه نمی‌دهد صفحه‌ی داخلی را ببینیم
function PrivateRoute({ children }) {
  const token = localStorage.getItem('accessToken');
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* روت اصلی را به لاگین می‌فرستیم */}
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/verify" element={<VerifyPage />} />
        <Route path="/login" element={<LoginPage />} />

        {/* /home فقط وقتی توکن داریم قابل دسترسی است */}
        <Route
          path="/home"
          element={
            <PrivateRoute>
              <HomePage />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
