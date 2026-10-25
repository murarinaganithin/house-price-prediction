import React from 'react';
import { Link } from 'react-router-dom';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="container">
      <main className="glass-panel not-found-container" id="not-found-card">
        <div className="not-found-code" id="not-found-error-code">404</div>
        <h2 className="not-found-title" id="not-found-error-title">Page Not Found</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
          The page you are looking for does not exist or has been moved.
        </p>
        <Link to="/" className="btn-primary" style={{ display: 'inline-flex', width: 'auto' }} id="btn-back-to-home">
          Back to Home
        </Link>
      </main>
    </div>
  );
};
