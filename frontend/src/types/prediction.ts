export interface PredictionRequest {
  location: string;
  carpet_area: number;
  bathroom: number;
  balcony: number;
  floor: string;
  furnishing: string;
  transaction: string;
  ownership: string;
  facing: string;
}

export interface PredictionResponse {
  predicted_price: number;
  currency: string;
  model_version: string;
}

export interface PredictionOptions {
  locations: string[];
  furnishing: string[];
  transaction: string[];
  ownership: string[];
  facing: string[];
}
