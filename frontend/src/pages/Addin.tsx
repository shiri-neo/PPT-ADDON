/**
 * Office Add-in page - Streamlined UI for PowerPoint users
 * This version is optimized for the PowerPoint taskpane
 */

import React, { useState } from 'react';
import DocumentUpload from '../components/DocumentUpload';
import DocumentList from '../components/DocumentList';
import PresentationGenerator from '../components/PresentationGenerator';
import Login from '../components/Login';

const Addin: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));
  const [selectedDocumentId, setSelectedDocumentId] = useState<number | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [activeTab, setActiveTab] = useState<'upload' | 'generate'>('upload');

  const handleLoginSuccess = (token: string) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  const handleUploadSuccess = () => {
    setRefreshTrigger(prev => prev + 1);
    setActiveTab('generate'); // Switch to generate tab after upload
  };

  if (!isAuthenticated) {
    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <h2 style={styles.title}>🤖 PPT AI Assistant</h2>
          <p style={styles.subtitle}>Sign in to start creating presentations</p>
        </div>
        <Login onLoginSuccess={handleLoginSuccess} />
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h2 style={styles.title}>🤖 PPT AI</h2>
          <p style={styles.subtitle}>AI-Powered Presentations</p>
        </div>
        <button onClick={handleLogout} style={styles.logoutButton}>
          Logout
        </button>
      </div>

      {/* Tab Navigation */}
      <div style={styles.tabs}>
        <button
          onClick={() => setActiveTab('upload')}
          style={{
            ...styles.tab,
            ...(activeTab === 'upload' ? styles.tabActive : {})
          }}
        >
          📤 Upload
        </button>
        <button
          onClick={() => setActiveTab('generate')}
          style={{
            ...styles.tab,
            ...(activeTab === 'generate' ? styles.tabActive : {})
          }}
        >
          ✨ Generate
        </button>
      </div>

      {/* Content */}
      <div style={styles.content}>
        {activeTab === 'upload' ? (
          <>
            <DocumentUpload onUploadSuccess={handleUploadSuccess} />
            <DocumentList
              onSelect={setSelectedDocumentId}
              selectedDocumentId={selectedDocumentId}
              refreshTrigger={refreshTrigger}
            />
          </>
        ) : (
          <>
            {!selectedDocumentId && (
              <div style={styles.notice}>
                <p>👈 Switch to the Upload tab to select a document first</p>
              </div>
            )}
            <PresentationGenerator
              selectedDocumentId={selectedDocumentId}
              onPresentationCreated={() => {
                // Presentation created successfully
                console.log('Presentation created in Add-in mode');
              }}
            />
          </>
        )}
      </div>

      {/* Footer */}
      <div style={styles.footer}>
        <small style={styles.footerText}>
          Powered by GPT-4 & DALL-E 3
        </small>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    backgroundColor: '#f5f5f5',
    fontFamily: 'Arial, sans-serif',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px',
    backgroundColor: '#0078d4',
    color: 'white',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  title: {
    margin: 0,
    fontSize: '18px',
    fontWeight: 600,
  },
  subtitle: {
    margin: '4px 0 0 0',
    fontSize: '12px',
    opacity: 0.9,
  },
  logoutButton: {
    padding: '6px 12px',
    backgroundColor: 'rgba(255,255,255,0.2)',
    color: 'white',
    border: '1px solid rgba(255,255,255,0.3)',
    borderRadius: '4px',
    fontSize: '12px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  tabs: {
    display: 'flex',
    backgroundColor: 'white',
    borderBottom: '1px solid #ddd',
  },
  tab: {
    flex: 1,
    padding: '12px',
    backgroundColor: 'transparent',
    border: 'none',
    borderBottom: '3px solid transparent',
    fontSize: '14px',
    fontWeight: 500,
    cursor: 'pointer',
    transition: 'all 0.2s',
    color: '#666',
  },
  tabActive: {
    color: '#0078d4',
    borderBottomColor: '#0078d4',
  },
  content: {
    flex: 1,
    overflow: 'auto',
    padding: '16px',
  },
  notice: {
    padding: '16px',
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '4px',
    marginBottom: '16px',
    textAlign: 'center',
  },
  footer: {
    padding: '12px',
    textAlign: 'center',
    backgroundColor: 'white',
    borderTop: '1px solid #ddd',
  },
  footerText: {
    color: '#666',
    fontSize: '11px',
  },
};

export default Addin;
