/**
 * Document list component
 */

import React, { useEffect, useState } from 'react';
import { documentsApi, Document } from '../api/documents';

interface DocumentListProps {
  onSelect?: (documentId: number) => void;
  selectedDocumentId?: number | null;
  refreshTrigger?: number;
}

const DocumentList: React.FC<DocumentListProps> = ({
  onSelect,
  selectedDocumentId,
  refreshTrigger,
}) => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDocuments = async () => {
    setLoading(true);
    setError('');
    try {
      const docs = await documentsApi.listDocuments();
      setDocuments(docs);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  const handleDocumentClick = (docId: number) => {
    if (onSelect) {
      onSelect(docId);
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <h3 style={styles.heading}>Documents</h3>
        <p>Loading documents...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.container}>
        <h3 style={styles.heading}>Documents</h3>
        <div style={styles.error}>{error}</div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Documents</h3>

      {documents.length === 0 ? (
        <p style={styles.emptyMessage}>No documents uploaded yet.</p>
      ) : (
        <ul style={styles.list}>
          {documents.map((doc) => (
            <li
              key={doc.id}
              onClick={() => handleDocumentClick(doc.id)}
              style={{
                ...styles.listItem,
                ...(selectedDocumentId === doc.id ? styles.selectedItem : {}),
              }}
            >
              <div style={styles.docName}>{doc.name}</div>
              <div style={styles.docDate}>
                {new Date(doc.created_at).toLocaleDateString()}
              </div>
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
  },
  selectedItem: {
    backgroundColor: '#e3f2fd',
    borderColor: '#0078d4',
  },
  docName: {
    fontWeight: 500,
    fontSize: '14px',
    marginBottom: '4px',
  },
  docDate: {
    fontSize: '12px',
    color: '#666',
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

export default DocumentList;
