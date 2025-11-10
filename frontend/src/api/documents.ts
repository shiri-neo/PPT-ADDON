/**
 * Document management API calls
 */

import apiClient from './client';

export interface Document {
  id: number;
  name: string;
  original_filename: string;
  created_at: string;
}

export interface DocumentUploadResponse {
  document: Document;
  message: string;
}

export const documentsApi = {
  /**
   * Upload a document
   */
  uploadDocument: async (file: File): Promise<DocumentUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<DocumentUploadResponse>(
      '/documents/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  /**
   * List all documents
   */
  listDocuments: async (): Promise<Document[]> => {
    const response = await apiClient.get<Document[]>('/documents');
    return response.data;
  },
};
