import React, { useState } from 'react';
import { Sidebar, Menu, MenuItem, useProSidebar } from 'react-pro-sidebar';
import { Avatar, IconButton, useMediaQuery } from '@mui/material';
import { Link } from 'react-router-dom';
import { Home, CalendarToday, BarChart, Map, Person, ExitToApp, Menu as MenuIcon } from '@mui/icons-material';

const SidebarComponent = () => {
  const [profilePic, setProfilePic] = useState(null);
  const { collapseSidebar, toggleSidebar, collapsed, broken } = useProSidebar();
  const isMobile = useMediaQuery('(max-width: 768px)'); // Detect mobile devices

  const handleProfilePicChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfilePic(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <Sidebar
        breakPoint="md" // Collapse sidebar on mobile devices
        style={{ height: '100vh' }}
      >
        <div className="sidebar-header">
          <Avatar
            src={profilePic || "https://via.placeholder.com/150"}
            sx={{ width: 80, height: 80 }}
          />
          <input
            type="file"
            accept="image/*"
            onChange={handleProfilePicChange}
            style={{ display: 'none' }}
            id="profile-pic-upload"
          />
          <label htmlFor="profile-pic-upload">
            <IconButton component="span">
              <Person />
            </IconButton>
          </label>
        </div>
        <Menu>
          <MenuItem icon={<Home />}>
            <Link to="/">Dashboard</Link>
          </MenuItem>
          <MenuItem icon={<CalendarToday />}>
            <Link to="/calendar">Calendar</Link>
          </MenuItem>
          <MenuItem icon={<BarChart />}>
            <Link to="/charts">Charts</Link>
          </MenuItem>
          <MenuItem icon={<Map />}>
            <Link to="/geography">Geography</Link>
          </MenuItem>
          <MenuItem icon={<ExitToApp />}>
            <Link to="/signin">Sign Out</Link>
          </MenuItem>
        </Menu>
      </Sidebar>

      <main style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>
        {/* Toggle Button */}
        <IconButton
          onClick={() => {
            if (isMobile) {
              toggleSidebar(); // Toggle sidebar on mobile
            } else {
              collapseSidebar(!collapsed); // Collapse/expand sidebar on desktop
            }
          }}
          sx={{ marginBottom: '20px' }}
        >
          <MenuIcon />
        </IconButton>

        {/* Your main content goes here */}
        <h1>Main Content</h1>
      </main>
    </div>
  );
};

export default SidebarComponent;