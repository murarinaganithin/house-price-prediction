import type { PredictionOptions, PredictionRequest, PredictionResponse } from '../types/prediction';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export class PredictionClientError extends Error {
  public type: 'connection' | 'validation' | 'generic';
  
  constructor(message: string, type: 'connection' | 'validation' | 'generic') {
    super(message);
    this.type = type;
    this.name = 'PredictionClientError';
  }
}

export async function getModelOptions(): Promise<PredictionOptions> {
  try {
    const response = await fetch(`${API_BASE_URL}/options`);
    if (!response.ok) {
      throw new PredictionClientError(
        'Unable to load property options. Please make sure the backend is running.',
        'generic'
      );
    }
    const data = await response.json();
    return data as PredictionOptions;
  } catch (error) {
    if (error instanceof PredictionClientError) {
      throw error;
    }
    throw new PredictionClientError(
      'Unable to load property options. Please make sure the backend is running.',
      'connection'
    );
  }
}

export async function predictHousePrice(data: PredictionRequest): Promise<PredictionResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new PredictionClientError(
        'Unable to calculate the house price. Please check your input and try again.',
        'validation'
      );
    }

    const result = await response.json();
    return result as PredictionResponse;
  } catch (error) {
    if (error instanceof PredictionClientError) {
      throw error;
    }
    throw new PredictionClientError(
      'Unable to connect to the prediction server. Please make sure the backend is running.',
      'connection'
    );
  }
}

export async function getSeedSample(): Promise<PredictionRequest> {
  try {
    const response = await fetch(`${API_BASE_URL}/seed`);
    if (!response.ok) {
      throw new PredictionClientError(
        'Unable to load sample data.',
        'generic'
      );
    }
    const data = await response.json();
    return data as PredictionRequest;
  } catch (error) {
    if (error instanceof PredictionClientError) {
      throw error;
    }
    throw new PredictionClientError(
      'Unable to connect to the prediction server.',
      'connection'
    );
  }
}
