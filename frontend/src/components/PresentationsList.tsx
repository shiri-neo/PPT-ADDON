/**
 * Presentations list component
 */

import React, { useEffect, useState } from 'react';
import { presentationsApi, Presentation } from '../api/presentations';
import { applySlides } from '../office/PowerPointIntegration';

interface PresentationsListProps {
  onSelect?: (presentationId: number) => void;
  selectedPresentationId?: number | null;
  refreshTrigger?: number;
}

const PresentationsList: React.FC<PresentationsListProps> = ({
  onSelect,
  selectedPresentationId,
  refreshTrigger,
}) => {
  const [presentations, setPresentations] = useState<Presentation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [applyingId, setApplyingId] = useState<number | null>(null);

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
    try {
      await applySlides(presentation.slides);
      alert(`Applied "${presentation.title}" to PowerPoint!`);
    } catch (err: any) {
      alert(`Failed to apply slides: ${err.message}`);
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

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Presentations</h3>

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
              <button
                onClick={(e) => handleApplyToPowerPoint(preso, e)}
                disabled={applyingId === preso.id}
                style={styles.applyButton}
              >
                {applyingId === preso.id ? 'Applying...' : 'Apply to PPT'}
              </button>
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
  emptyMessage: {
    color: '#666',
    fontSize: '14px',
  },
  error: {
    padding: '10px',
    backgroundColor: '#f8d7da',
    color: '#721c24',
    borderRadius: '4px',
    fontSize: '14px',
  },
};

export default PresentationsList;
