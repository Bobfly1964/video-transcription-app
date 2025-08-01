import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface TranscriptionRequest {
  url: string;
  topics: string[];
}

export interface TranscriptionResponse {
  jobId: string;
}

export interface TranscriptionStatus {
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  message?: string;
}

export interface Segment {
  timestamp: number;
  text: string;
}

export interface TranscriptionResult {
  segments: Segment[];
}

export interface Note {
  id: string;
  title: string;
  tags: string[];
  segments: Segment[];
  sourceUrl: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateNoteRequest {
  title: string;
  tags: string[];
  segments: Segment[];
  sourceUrl: string;
}

export const transcribeVideo = async (request: TranscriptionRequest): Promise<TranscriptionResponse> => {
  const response = await api.post('/transcribe', request);
  return response.data;
};

export const getTranscriptionStatus = async (jobId: string): Promise<TranscriptionStatus> => {
  const response = await api.get(`/transcribe/${jobId}/status`);
  return response.data;
};

export const getTranscriptionResult = async (jobId: string, topics: string[]): Promise<TranscriptionResult> => {
  const response = await api.get(`/transcribe/${jobId}/result`, {
    params: { topics: topics.join(',') },
  });
  return response.data;
};

export const getNotes = async (): Promise<Note[]> => {
  const response = await api.get('/notes');
  return response.data;
};

export const getNote = async (id: string): Promise<Note> => {
  const response = await api.get(`/notes/${id}`);
  return response.data;
};

export const createNote = async (note: CreateNoteRequest): Promise<Note> => {
  const response = await api.post('/notes', note);
  return response.data;
};

export const updateNote = async (id: string, note: Partial<CreateNoteRequest>): Promise<Note> => {
  const response = await api.put(`/notes/${id}`, note);
  return response.data;
};

export const deleteNote = async (id: string): Promise<void> => {
  await api.delete(`/notes/${id}`);
}; 