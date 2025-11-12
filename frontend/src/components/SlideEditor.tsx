/**
 * Slide editor component
 */

import React, { useState } from 'react';
import { presentationsApi } from '../api/presentations';
import { updateSlide } from '../office/PowerPointIntegration';

interface SlideEditorProps {
  presentationId: number | null;
}

const SlideEditor: React.FC<SlideEditorProps> = ({ presentationId }) => {
  const [slideIndex, setSlideIndex] = useState(0);
  const [instruction, setInstruction] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [buttonHover, setButtonHover] = useState(false);

  const handleEdit = async () => {
    if (!presentationId) {
      setError('No presentation available. Please generate one first.');
      return;
    }

    if (!instruction.trim()) {
      setError('Please enter an edit instruction');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    try {
      // Call API to edit slide
      const response = await presentationsApi.editSlide(
        presentationId,
        slideIndex,
        instruction
      );

      // Update slide in PowerPoint
      await updateSlide(slideIndex, response.slide);

      setMessage(response.message);
      setInstruction('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to edit slide. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Edit Slide</h3>

      {!presentationId && (
        <div style={styles.warning}>
          Please generate a presentation first before editing slides.
        </div>
      )}

      <div style={styles.form}>
        <div style={styles.inputGroup}>
          <label style={styles.label}>Slide Index (0-based):</label>
          <input
            type="number"
            min={0}
            value={slideIndex}
            onChange={(e) => setSlideIndex(parseInt(e.target.value))}
            style={styles.input}
            disabled={!presentationId}
          />
          <small style={styles.hint}>Index starts at 0 (first slide = 0, second = 1, etc.)</small>
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Edit Instruction:</label>
          <textarea
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            placeholder="E.g., Make it more concise, Add emphasis on key points, etc."
            style={styles.textarea}
            rows={4}
            disabled={!presentationId}
          />
        </div>

        <button
          onClick={handleEdit}
          disabled={loading || !presentationId}
          style={{
            ...styles.button,
            ...(loading || !presentationId ? styles.buttonDisabled : {}),
            ...(buttonHover && !loading && presentationId ? styles.buttonHover : {}),
          }}
          onMouseEnter={() => setButtonHover(true)}
          onMouseLeave={() => setButtonHover(false)}
        >
          {loading ? 'Applying Edit...' : 'Apply Edit'}
        </button>
      </div>

      {message && <div style={styles.success}>{message}</div>}
      {error && <div style={styles.error}>{error}</div>}
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
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
  label: {
    fontSize: '14px',
    fontWeight: 500,
  },
  input: {
    padding: '8px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
  },
  textarea: {
    padding: '8px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontFamily: 'inherit',
    resize: 'vertical',
  },
  hint: {
    fontSize: '12px',
    color: '#666',
  },
  button: {
    padding: '12px',
    backgroundColor: '#0078d4',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    fontSize: '14px',
    fontWeight: 500,
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
    cursor: 'not-allowed',
    opacity: 0.6,
  },
  buttonHover: {
    backgroundColor: '#106ebe',
    transform: 'translateY(-1px)',
    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
  },
  warning: {
    padding: '10px',
    backgroundColor: '#fff3cd',
    color: '#856404',
    borderRadius: '4px',
    fontSize: '14px',
    marginBottom: '15px',
  },
  success: {
    marginTop: '15px',
    padding: '10px',
    backgroundColor: '#d4edda',
    color: '#155724',
    borderRadius: '4px',
    fontSize: '14px',
  },
  error: {
    marginTop: '15px',
    padding: '10px',
    backgroundColor: '#f8d7da',
    color: '#721c24',
    borderRadius: '4px',
    fontSize: '14px',
  },
};

export default SlideEditor;
