/**
 * Presentation generation and editing API calls
 */

import apiClient from './client';

export interface Slide {
  title: string;
  bullets: string[];
  notes?: string;
}

export interface Presentation {
  id: number;
  title: string;
  created_at: string;
  slides: Slide[];
}

export interface PresentationCreateRequest {
  document_id: number;
  slide_count: number;
  tone?: string;
}

export interface SlideEditRequest {
  instruction: string;
}

export interface SlideEditResponse {
  slide: Slide;
  message: string;
}

export const presentationsApi = {
  /**
   * Create presentation from document
   */
  createPresentationFromDocument: async (
    data: PresentationCreateRequest
  ): Promise<Presentation> => {
    const response = await apiClient.post<Presentation>(
      '/presentations/from-document',
      data
    );
    return response.data;
  },

  /**
   * Edit a specific slide
   */
  editSlide: async (
    presentationId: number,
    slideIndex: number,
    instruction: string
  ): Promise<SlideEditResponse> => {
    const response = await apiClient.post<SlideEditResponse>(
      `/presentations/${presentationId}/slides/${slideIndex}/edit`,
      { instruction }
    );
    return response.data;
  },
};
