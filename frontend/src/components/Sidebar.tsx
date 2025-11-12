/**
 * Sidebar navigation component
 */

import React from 'react';
import { useAuth } from '../context/AuthContext';

interface SidebarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentPage, onNavigate }) => {
  const { logout } = useAuth();

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'documents', label: 'Documents', icon: '📄' },
    { id: 'presentations', label: 'Presentations', icon: '📽️' },
    { id: 'settings', label: 'Company Settings', icon: '⚙️' },
    { id: 'users', label: 'User Management', icon: '👥' },
  ];

  return (
    <div style={styles.sidebar}>
      <div style={styles.header}>
        <h2 style={styles.logo}>📊 PPT AI</h2>
      </div>

      <nav style={styles.nav}>
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            style={{
              ...styles.navItem,
              ...(currentPage === item.id ? styles.navItemActive : {}),
            }}
          >
            <span style={styles.icon}>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div style={styles.footer}>
        <button onClick={logout} style={styles.logoutButton}>
          🚪 Logout
        </button>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  sidebar: {
    width: '250px',
    height: '100vh',
    backgroundColor: '#1e1e1e',
    color: 'white',
    display: 'flex',
    flexDirection: 'column',
    position: 'fixed',
    left: 0,
    top: 0,
  },
  header: {
    padding: '20px',
    borderBottom: '1px solid #333',
  },
  logo: {
    margin: 0,
    fontSize: '20px',
    fontWeight: 600,
  },
  nav: {
    flex: 1,
    padding: '20px 0',
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
  navItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '12px 20px',
    backgroundColor: 'transparent',
    color: '#ccc',
    borderTop: '0',
    borderRight: '0',
    borderBottom: '0',
    borderLeft: '0',
    textAlign: 'left',
    cursor: 'pointer',
    fontSize: '14px',
    transition: 'all 0.2s',
  },
  navItemActive: {
    backgroundColor: '#0078d4',
    color: 'white',
    borderTop: '0',
    borderRight: '0',
    borderBottom: '0',
    borderLeft: '4px solid #fff',
  },
  icon: {
    fontSize: '18px',
  },
  footer: {
    padding: '20px',
    borderTop: '1px solid #333',
  },
  logoutButton: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#d32f2f',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 500,
  },
};

export default Sidebar;
