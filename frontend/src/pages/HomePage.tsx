import React, { useEffect, useState, useRef } from 'react';
import type { PredictionOptions } from '../types/prediction';
import { getModelOptions, PredictionClientError } from '../api/predictionClient';
import { PredictionForm } from '../components/PredictionForm';

export const HomePage: React.FC = () => {
  const [options, setOptions] = useState<PredictionOptions | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const formRef = useRef<{ fillSeed: () => void }>(null);

  const fetchOptions = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getModelOptions();
      setOptions(data);
    } catch (err) {
      if (err instanceof PredictionClientError) {
        setError(err.message);
      } else {
        setError('Unable to load property options. Please make sure the backend is running.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOptions();
  }, []);

  const handleQuickFill = async () => {
    if (formRef.current) {
      formRef.current.fillSeed();
    }
  };

  return (
    <div className="container">
      {/* Floating Quick Fill button — only visible when form is loaded */}
      {!loading && !error && options && (
        <button
          className="quick-fill-btn"
          onClick={handleQuickFill}
          type="button"
          id="btn-quick-fill"
          title="Fill with random sample data"
        >
          <span className="dice-icon">🎲</span>
          <span className="btn-label">Quick Fill</span>
        </button>
      )}

      <header style={{ marginBottom: '24px' }}>
        <h1>HOUSE PRICE PREDICTION</h1>
        <p className="subtitle">AI-powered property price estimation</p>
      </header>

      <main className="glass-panel">
        {loading && (
          <div className="loader-wrapper" id="options-loading-indicator">
            <div className="spinner" aria-hidden="true" />
            <p>Loading property options...</p>
          </div>
        )}

        {error && (
          <div className="alert alert-danger" role="alert" id="options-error-alert">
            <h4>Failed to Load Options</h4>
            <p>{error}</p>
            <button
              onClick={fetchOptions}
              className="btn-secondary"
              style={{ marginTop: '12px' }}
              type="button"
              id="btn-retry-options"
            >
              Retry
            </button>
          </div>
        )}

        {!loading && !error && options && (
          <PredictionForm options={options} ref={formRef} />
        )}
      </main>
    </div>
  );
};
