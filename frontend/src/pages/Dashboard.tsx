/**
 * Dashboard page - overview and stats
 */

import React, { useEffect, useState } from 'react';
import { documentsApi } from '../api/documents';
import { presentationsApi } from '../api/presentations';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    documents: 0,
    presentations: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [docs, presos] = await Promise.all([
        documentsApi.listDocuments(),
        presentationsApi.listPresentations(),
      ]);

      setStats({
        documents: docs.length,
        presentations: presos.length,
      });
    } catch (err) {
      console.error('Failed to load stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={styles.container}><p>Loading...</p></div>;
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Dashboard</h1>
      <p style={styles.subtitle}>Welcome to your PPT AI workspace</p>

      <div style={styles.statsGrid}>
        <div style={styles.statCard}>
          <div style={styles.statIcon}>📄</div>
          <div style={styles.statContent}>
            <div style={styles.statValue}>{stats.documents}</div>
            <div style={styles.statLabel}>Documents Uploaded</div>
          </div>
        </div>

        <div style={styles.statCard}>
          <div style={styles.statIcon}>📽️</div>
          <div style={styles.statContent}>
            <div style={styles.statValue}>{stats.presentations}</div>
            <div style={styles.statLabel}>Presentations Created</div>
          </div>
        </div>

        <div style={styles.statCard}>
          <div style={styles.statIcon}>🤖</div>
          <div style={styles.statContent}>
            <div style={styles.statValue}>AI Powered</div>
            <div style={styles.statLabel}>Smart Analysis Enabled</div>
          </div>
        </div>
      </div>

      <div style={styles.quickActions}>
        <h2 style={styles.sectionTitle}>Quick Actions</h2>
        <div style={styles.actionsGrid}>
          <div style={styles.actionCard}>
            <h3 style={styles.actionTitle}>📤 Upload Document</h3>
            <p style={styles.actionDesc}>Upload a PDF, DOCX, TXT, or PPTX file to get started</p>
          </div>

          <div style={styles.actionCard}>
            <h3 style={styles.actionTitle}>✨ Generate Presentation</h3>
            <p style={styles.actionDesc}>Let AI create branded slides from your documents</p>
          </div>

          <div style={styles.actionCard}>
            <h3 style={styles.actionTitle}>⚙️ Configure Branding</h3>
            <p style={styles.actionDesc}>Set your company colors, logo, and design style</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    padding: '30px',
    maxWidth: '1200px',
  },
  title: {
    fontSize: '32px',
    fontWeight: 700,
    margin: '0 0 10px 0',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    margin: '0 0 30px 0',
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '40px',
  },
  statCard: {
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
    padding: '24px',
    backgroundColor: 'white',
    border: '1px solid #e0e0e0',
    borderRadius: '12px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
  },
  statIcon: {
    fontSize: '40px',
  },
  statContent: {
    flex: 1,
  },
  statValue: {
    fontSize: '28px',
    fontWeight: 700,
    color: '#0078d4',
    marginBottom: '4px',
  },
  statLabel: {
    fontSize: '14px',
    color: '#666',
  },
  quickActions: {
    marginTop: '40px',
  },
  sectionTitle: {
    fontSize: '24px',
    fontWeight: 600,
    marginBottom: '20px',
  },
  actionsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '20px',
  },
  actionCard: {
    padding: '24px',
    backgroundColor: '#f8f9fa',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  actionTitle: {
    fontSize: '18px',
    fontWeight: 600,
    margin: '0 0 8px 0',
  },
  actionDesc: {
    fontSize: '14px',
    color: '#666',
    margin: 0,
  },
};

export default Dashboard;
