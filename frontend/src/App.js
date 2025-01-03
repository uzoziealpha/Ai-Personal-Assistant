import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ProSidebarProvider } from 'react-pro-sidebar'; // Import ProSidebarProvider
import Sidebar from './components/Sidebar/Sidebar';
import Navbar from './components/Navbar/Navbar';
import Dashboard from './pages/Dashboard/Dashboard';
import SignIn from './pages/SignIn/SignIn';
import SignUp from './pages/SignUp/SignUp';

const App = () => {
  return (
    <ProSidebarProvider> {/* Wrap your app with ProSidebarProvider */}
      <Router>
        <div style={{ display: 'flex' }}>
          <Sidebar />
          <div style={{ flex: 1 }}>
            <Navbar />
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/signin" element={<SignIn />} />
              <Route path="/signup" element={<SignUp />} />
            </Routes>
          </div>
        </div>
      </Router>
    </ProSidebarProvider>
  );
};

export default App;