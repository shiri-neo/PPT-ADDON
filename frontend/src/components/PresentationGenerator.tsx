/**
 * Presentation generator component
 */

import React, { useState } from 'react';
import { presentationsApi } from '../api/presentations';
import { applySlides } from '../office/PowerPointIntegration';

interface PresentationGeneratorProps {
  selectedDocumentId: number | null;
  onPresentationCreated?: (presentationId: number) => void;
}

const PresentationGenerator: React.FC<PresentationGeneratorProps> = ({
  selectedDocumentId,
  onPresentationCreated,
}) => {
  const [slideCount, setSlideCount] = useState(5);
  const [tone, setTone] = useState('formal');
  const [customInstructions, setCustomInstructions] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [buttonHover, setButtonHover] = useState(false);

  const handleGenerate = async () => {
    if (!selectedDocumentId) {
      setError('Please select a document first');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');

    try {
      // Call API to generate presentation with custom instructions
      const presentation = await presentationsApi.createPresentationFromDocument({
        document_id: selectedDocumentId,
        slide_count: slideCount,
        tone: tone,
        custom_instructions: customInstructions || undefined,
      });

      // Apply slides to PowerPoint
      await applySlides(presentation.slides);

      setMessage(
        `Presentation "${presentation.title}" created with ${presentation.slides.length} slides!`
      );

      // Notify parent component
      if (onPresentationCreated) {
        onPresentationCreated(presentation.id);
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Failed to generate presentation. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Generate Presentation</h3>

      {!selectedDocumentId && (
        <div style={styles.warning}>Please select a document to generate a presentation.</div>
      )}

      <div style={styles.form}>
        <div style={styles.inputGroup}>
          <label style={styles.label}>Number of Slides:</label>
          <input
            type="number"
            min={1}
            max={20}
            value={slideCount}
            onChange={(e) => setSlideCount(parseInt(e.target.value) || 5)}
            style={styles.input}
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Tone:</label>
          <select value={tone} onChange={(e) => setTone(e.target.value)} style={styles.select}>
            <option value="formal">Formal</option>
            <option value="casual">Casual</option>
            <option value="marketing">Marketing</option>
            <option value="academic">Academic</option>
          </select>
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Custom Instructions (Optional):</label>
          <textarea
            value={customInstructions}
            onChange={(e) => setCustomInstructions(e.target.value)}
            placeholder="E.g., 'Focus on financial data', 'Include more charts', 'Use simple language', etc."
            style={styles.textarea}
            rows={3}
          />
          <span style={styles.helpText}>
            Tell the AI how you want your presentation to look and what to focus on
          </span>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading || !selectedDocumentId}
          style={{
            ...styles.button,
            ...(loading || !selectedDocumentId ? styles.buttonDisabled : {}),
            ...(buttonHover && !loading && selectedDocumentId ? styles.buttonHover : {}),
          }}
          onMouseEnter={() => setButtonHover(true)}
          onMouseLeave={() => setButtonHover(false)}
        >
          {loading ? 'Generating...' : 'Generate Presentation'}
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
  select: {
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
    resize: 'vertical' as const,
    width: '100%',
    boxSizing: 'border-box' as const,
  },
  helpText: {
    fontSize: '12px',
    color: '#666',
    marginTop: '4px',
    display: 'block',
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

export default PresentationGenerator;
