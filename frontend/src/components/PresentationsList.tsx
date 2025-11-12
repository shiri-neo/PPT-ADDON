/**
 * Presentations list component
 */

import React, { useEffect, useState } from 'react';
import { presentationsApi, Presentation } from '../api/presentations';
import { applySlides } from '../office/PowerPointIntegration';
import apiClient from '../api/client';

interface PresentationsListProps {
  onSelect?: (presentationId: number) => void;
  selectedPresentationId?: number | null;
  refreshTrigger?: number;
}

// Check if we're running in PowerPoint
const isInPowerPoint = (): boolean => {
  return typeof PowerPoint !== 'undefined' && PowerPoint !== null;
};

const PresentationsList: React.FC<PresentationsListProps> = ({
  onSelect,
  selectedPresentationId,
  refreshTrigger,
}) => {
  const [presentations, setPresentations] = useState<Presentation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [applyingId, setApplyingId] = useState<number | null>(null);
  const [successMessage, setSuccessMessage] = useState('');

  const fetchPresentations = async () => {
    setLoading(true);
    setError('');
    try {
      const presos = await presentationsApi.listPresentations();
      setPresentations(presos);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load presentations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPresentations();
  }, [refreshTrigger]);

  const handlePresentationClick = (presoId: number) => {
    if (onSelect) {
      onSelect(presoId);
    }
  };

  const handleApplyToPowerPoint = async (presentation: Presentation, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent triggering the click handler
    setApplyingId(presentation.id);
    setSuccessMessage('');
    setError('');

    try {
      await applySlides(presentation.slides);
      console.log(`✅ Applied "${presentation.title}" to PowerPoint!`);
      setSuccessMessage(`Applied "${presentation.title}" to PowerPoint!`);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err: any) {
      console.error('❌ Failed to apply slides:', err);
      setError(`Failed to apply slides: ${err.message}`);
    } finally {
      setApplyingId(null);
    }
  };

  const handleDownloadPPTX = async (presentation: Presentation, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent triggering the click handler
    setApplyingId(presentation.id);
    setSuccessMessage('');
    setError('');

    try {
      // Get the auth token
      const token = localStorage.getItem('token');

      // Download the file
      const response = await fetch(
        `${apiClient.defaults.baseURL}/presentations/${presentation.id}/download`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to download presentation');
      }

      // Create a blob from the response
      const blob = await response.blob();

      // Create a download link and trigger it
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${presentation.title}.pptx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      console.log(`✅ Downloaded "${presentation.title}.pptx"`);
      setSuccessMessage(`Downloaded "${presentation.title}.pptx"`);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err: any) {
      console.error('❌ Failed to download presentation:', err);
      setError(`Failed to download: ${err.message}`);
    } finally {
      setApplyingId(null);
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <h3 style={styles.heading}>Presentations</h3>
        <p>Loading presentations...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.container}>
        <h3 style={styles.heading}>Presentations</h3>
        <div style={styles.error}>{error}</div>
      </div>
    );
  }

  const inPowerPoint = isInPowerPoint();

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>
        Presentations {!inPowerPoint && <span style={styles.browserBadge}>(Browser Mode)</span>}
      </h3>

      {successMessage && <div style={styles.success}>{successMessage}</div>}
      {error && <div style={styles.error}>{error}</div>}

      {presentations.length === 0 ? (
        <p style={styles.emptyMessage}>No presentations created yet.</p>
      ) : (
        <ul style={styles.list}>
          {presentations.map((preso) => (
            <li
              key={preso.id}
              onClick={() => handlePresentationClick(preso.id)}
              style={{
                ...styles.listItem,
                ...(selectedPresentationId === preso.id ? styles.selectedItem : {}),
              }}
            >
              <div style={styles.presoInfo}>
                <div style={styles.presoName}>{preso.title}</div>
                <div style={styles.presoMeta}>
                  {preso.slides.length} slides • {new Date(preso.created_at).toLocaleDateString()}
                </div>
              </div>

              {inPowerPoint ? (
                <button
                  onClick={(e) => handleApplyToPowerPoint(preso, e)}
                  disabled={applyingId === preso.id}
                  style={styles.applyButton}
                >
                  {applyingId === preso.id ? 'Applying...' : 'Apply to PPT'}
                </button>
              ) : (
                <button
                  onClick={(e) => handleDownloadPPTX(preso, e)}
                  disabled={applyingId === preso.id}
                  style={styles.downloadButton}
                >
                  {applyingId === preso.id ? 'Downloading...' : 'Download PPTX'}
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    marginBottom: '30px',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
  },
  heading: {
    marginTop: 0,
    marginBottom: '15px',
    fontSize: '18px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  browserBadge: {
    fontSize: '12px',
    fontWeight: 'normal',
    color: '#666',
    backgroundColor: '#e0e0e0',
    padding: '2px 8px',
    borderRadius: '4px',
  },
  list: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  listItem: {
    padding: '12px',
    marginBottom: '8px',
    backgroundColor: 'white',
    border: '1px solid #ddd',
    borderRadius: '4px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  selectedItem: {
    backgroundColor: '#e3f2fd',
    borderColor: '#0078d4',
  },
  presoInfo: {
    flex: 1,
  },
  presoName: {
    fontWeight: 500,
    fontSize: '14px',
    marginBottom: '4px',
  },
  presoMeta: {
    fontSize: '12px',
    color: '#666',
  },
  applyButton: {
    padding: '6px 12px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: 500,
    cursor: 'pointer',
    marginLeft: '10px',
  },
  downloadButton: {
    padding: '6px 12px',
    backgroundColor: '#0078d4',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: 500,
    cursor: 'pointer',
    marginLeft: '10px',
  },
  emptyMessage: {
    color: '#666',
    fontSize: '14px',
  },
  success: {
    marginBottom: '15px',
    padding: '10px',
    backgroundColor: '#d4edda',
    color: '#155724',
    borderRadius: '4px',
    fontSize: '14px',
  },
  error: {
    marginBottom: '15px',
    padding: '10px',
    backgroundColor: '#f8d7da',
    color: '#721c24',
    borderRadius: '4px',
    fontSize: '14px',
  },
};

export default PresentationsList;
