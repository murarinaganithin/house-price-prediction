import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import type { PredictionResponse } from '../types/prediction';

export const ResultPage: React.FC = () => {
  const location = useLocation();
  const result = location.state as PredictionResponse | null;

  const formatPrice = (price: number): string => {
    const formatter = new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    });
    return formatter.format(price);
  };

  return (
    <div className="container">
      <header style={{ marginBottom: '24px' }}>
        <h1>HOUSE PRICE PREDICTION</h1>
        <p className="subtitle">AI-powered property price estimation</p>
      </header>

      <main className="glass-panel" id="result-card">
        {result ? (
          <div className="result-container">
            <h2 className="result-meta-label" style={{ fontSize: '1rem', letterSpacing: '0.1em' }}>
              Estimated House Price
            </h2>
            <div className="result-glow-box">
              <div className="result-price" id="predicted-price-value">
                {formatPrice(result.predicted_price)}
              </div>
            </div>
            
            <div className="result-metadata">
              <div className="result-meta-item">
                <span className="result-meta-label">Currency</span>
                <span className="result-meta-value" id="result-currency">
                  {result.currency || 'INR'}
                </span>
              </div>
              <div className="result-meta-item">
                <span className="result-meta-label">Model Version</span>
                <span className="result-meta-value" id="result-model-version">
                  {result.model_version || '1.0'}
                </span>
              </div>
            </div>

            <Link to="/" className="btn-secondary" id="btn-predict-another">
              Predict Another Property
            </Link>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '24px 0' }}>
            <h3 style={{ marginBottom: '16px', color: '#fca5a5' }} id="no-result-message">
              No prediction result is available.
            </h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
              Please enter your property details to get an AI-powered price estimate.
            </p>
            <Link to="/" className="btn-primary" style={{ display: 'inline-flex', width: 'auto' }} id="btn-make-prediction-redirect">
              Make a Prediction
            </Link>
          </div>
        )}
      </main>
    </div>
  );
};
