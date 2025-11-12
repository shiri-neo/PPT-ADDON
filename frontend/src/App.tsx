/**
 * Main App component
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from './context/AuthContext';
import { initializeOffice } from './office/office-init';
import Layout from './components/Layout';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import CompanySettings from './pages/CompanySettings';
import DocumentUpload from './components/DocumentUpload';
import DocumentList from './components/DocumentList';
import PresentationGenerator from './components/PresentationGenerator';
import PresentationsList from './components/PresentationsList';
import SlideEditor from './components/SlideEditor';

const App: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
  const [officeReady, setOfficeReady] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [selectedDocumentId, setSelectedDocumentId] = useState<number | null>(null);
  const [currentPresentationId, setCurrentPresentationId] = useState<number | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [presentationsRefreshTrigger, setPresentationsRefreshTrigger] = useState(0);

  useEffect(() => {
    // Initialize Office.js
    initializeOffice()
      .then(() => {
        setOfficeReady(true);
        console.log('Office.js initialized');
      })
      .catch((err) => {
        console.error('Office.js initialization failed:', err);
        // Still allow the app to work for testing outside PowerPoint
        setOfficeReady(true);
      });
  }, []);

  const handleUploadSuccess = () => {
    // Refresh document list
    setRefreshTrigger((prev) => prev + 1);
  };

  const handlePresentationCreated = (presentationId: number) => {
    setCurrentPresentationId(presentationId);
    // Refresh presentations list
    setPresentationsRefreshTrigger((prev) => prev + 1);
  };

  if (!officeReady) {
    return (
      <div style={styles.loading}>
        <p>Initializing Office Add-in...</p>
      </div>
    );
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;

      case 'documents':
        return (
          <div style={styles.pageContent}>
            <DocumentUpload onUploadSuccess={handleUploadSuccess} />
            <DocumentList
              onSelect={setSelectedDocumentId}
              selectedDocumentId={selectedDocumentId}
              refreshTrigger={refreshTrigger}
            />
            <PresentationGenerator
              selectedDocumentId={selectedDocumentId}
              onPresentationCreated={handlePresentationCreated}
            />
          </div>
        );

      case 'presentations':
        return (
          <div style={styles.pageContent}>
            <PresentationsList
              onSelect={setCurrentPresentationId}
              selectedPresentationId={currentPresentationId}
              refreshTrigger={presentationsRefreshTrigger}
            />
            <SlideEditor presentationId={currentPresentationId} />
          </div>
        );

      case 'settings':
        return <CompanySettings />;

      case 'users':
        return (
          <div style={styles.pageContent}>
            <h1>User Management</h1>
            <p>User management coming soon...</p>
          </div>
        );

      default:
        return <Dashboard />;
    }
  };

  return (
    <>
      {!isAuthenticated ? (
        <Layout>
          <div style={styles.authContainer}>
            <div style={styles.authTabs}>
              <button
                onClick={() => setAuthMode('login')}
                style={{
                  ...styles.tabButton,
                  ...(authMode === 'login' ? styles.activeTab : {}),
                }}
              >
                Login
              </button>
              <button
                onClick={() => setAuthMode('signup')}
                style={{
                  ...styles.tabButton,
                  ...(authMode === 'signup' ? styles.activeTab : {}),
                }}
              >
                Sign Up
              </button>
            </div>

            {authMode === 'login' ? <LoginForm /> : <SignupForm />}
          </div>
        </Layout>
      ) : (
        <div style={styles.appContainer}>
          <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
          <div style={styles.mainContent}>
            {renderPage()}
          </div>
        </div>
      )}
    </>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    fontSize: '16px',
  },
  authContainer: {
    maxWidth: '500px',
    margin: '50px auto',
  },
  authTabs: {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px',
    justifyContent: 'center',
  },
  tabButton: {
    padding: '10px 30px',
    backgroundColor: '#f0f0f0',
    border: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: 'pointer',
    fontWeight: 500,
  },
  activeTab: {
    backgroundColor: '#0078d4',
    color: 'white',
  },
  appContainer: {
    display: 'flex',
    height: '100vh',
    backgroundColor: '#f5f5f5',
  },
  mainContent: {
    marginLeft: '250px',
    flex: 1,
    overflowY: 'auto',
    backgroundColor: '#f5f5f5',
  },
  pageContent: {
    padding: '30px',
    maxWidth: '1200px',
  },
};

export default App;
