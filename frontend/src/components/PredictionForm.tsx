import React, { useState, useMemo, forwardRef, useImperativeHandle } from 'react';
import { useNavigate } from 'react-router-dom';
import type { PredictionOptions, PredictionRequest } from '../types/prediction';
import { predictHousePrice, getSeedSample, PredictionClientError } from '../api/predictionClient';

interface PredictionFormProps {
  options: PredictionOptions;
}

interface FormErrors {
  [key: string]: string;
}

/**
 * Sort options alphabetically, but push special values like "Other", "Unknown"
 * to the very end of the list.
 */
function sortWithSpecialLast(items: string[]): string[] {
  const specialValues = new Set(['other', 'unknown']);
  const normal: string[] = [];
  const special: string[] = [];

  for (const item of items) {
    if (specialValues.has(item.toLowerCase())) {
      special.push(item);
    } else {
      normal.push(item);
    }
  }

  normal.sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));
  special.sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));

  return [...normal, ...special];
}

export interface PredictionFormHandle {
  fillSeed: () => void;
}

export const PredictionForm = forwardRef<PredictionFormHandle, PredictionFormProps>(({ options }, ref) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<PredictionRequest>({
    location: '',
    carpet_area: 0,
    bathroom: 1,
    balcony: 0,
    floor: '',
    furnishing: '',
    transaction: '',
    ownership: '',
    facing: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  // Pre-sort all dropdown options
  const sortedLocations = useMemo(() => sortWithSpecialLast(options.locations), [options.locations]);
  const sortedFurnishing = useMemo(() => sortWithSpecialLast(options.furnishing), [options.furnishing]);
  const sortedTransaction = useMemo(() => sortWithSpecialLast(options.transaction), [options.transaction]);
  const sortedOwnership = useMemo(() => sortWithSpecialLast(options.ownership), [options.ownership]);
  const sortedFacing = useMemo(() => sortWithSpecialLast(options.facing), [options.facing]);

  const validate = (): boolean => {
    const tempErrors: FormErrors = {};

    if (!formData.location) {
      tempErrors.location = 'Please select a location.';
    }
    
    if (formData.carpet_area === undefined || formData.carpet_area <= 0) {
      tempErrors.carpet_area = 'Carpet area must be greater than 0.';
    }
    
    if (formData.bathroom === undefined || formData.bathroom <= 0 || !Number.isInteger(Number(formData.bathroom))) {
      tempErrors.bathroom = 'Bathroom count must be greater than 0.';
    }
    
    if (formData.balcony === undefined || formData.balcony < 0 || !Number.isInteger(Number(formData.balcony))) {
      tempErrors.balcony = 'Balcony count cannot be negative.';
    }
    
    if (!formData.floor.trim()) {
      tempErrors.floor = 'Please enter the floor.';
    }
    
    if (!formData.furnishing) {
      tempErrors.furnishing = 'Please select a furnishing type.';
    }
    
    if (!formData.transaction) {
      tempErrors.transaction = 'Please select a transaction type.';
    }
    
    if (!formData.ownership) {
      tempErrors.ownership = 'Please select an ownership type.';
    }
    
    if (!formData.facing) {
      tempErrors.facing = 'Please select the property facing.';
    }

    setErrors(tempErrors);
    return Object.keys(tempErrors).length === 0;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? '' : Number(value)) : value,
    }));
    
    // Clear field-specific validation error on change
    if (errors[name]) {
      setErrors((prev) => {
        const copy = { ...prev };
        delete copy[name];
        return copy;
      });
    }
  };

  const handleQuickFill = async () => {
    try {
      const seed = await getSeedSample();
      setFormData(seed);
      setErrors({});
      setApiError(null);

      // Add flash animation to all inputs
      const inputs = document.querySelectorAll('input, select');
      inputs.forEach((el) => {
        el.classList.remove('field-flash');
        // Force reflow to restart animation
        void (el as HTMLElement).offsetWidth;
        el.classList.add('field-flash');
      });
    } catch {
      // Silently fail — the button is a convenience feature
    }
  };

  // Expose fillSeed to parent via ref
  useImperativeHandle(ref, () => ({
    fillSeed: handleQuickFill,
  }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setApiError(null);

    if (!validate()) {
      return;
    }

    setLoading(true);
    try {
      const response = await predictHousePrice(formData);
      navigate('/result', { state: response });
    } catch (err) {
      if (err instanceof PredictionClientError) {
        setApiError(err.message);
      } else {
        setApiError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      {apiError && (
        <div className="alert alert-danger" role="alert" id="api-error-alert">
          <h4>Prediction Error</h4>
          <p>{apiError}</p>
        </div>
      )}

      <div className="form-grid">
        {/* Location select */}
        <div className="form-group col-span-2">
          <label htmlFor="location">Location</label>
          <select
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.location ? 'input-error' : ''}
            required
          >
            <option value="">Select Location</option>
            {sortedLocations.map((loc) => (
              <option key={loc} value={loc}>
                {loc}
              </option>
            ))}
          </select>
          {errors.location && (
            <span className="error-text" id="error-location">
              {errors.location}
            </span>
          )}
        </div>

        {/* Carpet Area input */}
        <div className="form-group col-span-2">
          <label htmlFor="carpet_area">Carpet Area</label>
          <div className="input-with-unit">
            <input
              type="number"
              id="carpet_area"
              name="carpet_area"
              placeholder="e.g. 1200"
              value={formData.carpet_area || ''}
              onChange={handleInputChange}
              disabled={loading}
              className={errors.carpet_area ? 'input-error' : ''}
              required
              min="1"
            />
            <span className="input-unit">sq.ft</span>
          </div>
          {errors.carpet_area && (
            <span className="error-text" id="error-carpet-area">
              {errors.carpet_area}
            </span>
          )}
        </div>

        {/* Bathroom & Balcony row */}
        <div className="form-group">
          <label htmlFor="bathroom">Bathroom</label>
          <input
            type="number"
            id="bathroom"
            name="bathroom"
            value={formData.bathroom}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.bathroom ? 'input-error' : ''}
            required
            min="1"
            step="1"
          />
          {errors.bathroom && (
            <span className="error-text" id="error-bathroom">
              {errors.bathroom}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="balcony">Balcony</label>
          <input
            type="number"
            id="balcony"
            name="balcony"
            value={formData.balcony}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.balcony ? 'input-error' : ''}
            required
            min="0"
            step="1"
          />
          {errors.balcony && (
            <span className="error-text" id="error-balcony">
              {errors.balcony}
            </span>
          )}
        </div>

        {/* Floor input */}
        <div className="form-group col-span-2">
          <label htmlFor="floor">Floor</label>
          <input
            type="text"
            id="floor"
            name="floor"
            placeholder="5 out of 10"
            value={formData.floor}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.floor ? 'input-error' : ''}
            required
          />
          <span className="helper-text">
            Example: 5 out of 10, Ground, Upper Basement
          </span>
          {errors.floor && (
            <span className="error-text" id="error-floor">
              {errors.floor}
            </span>
          )}
        </div>

        {/* Furnishing & Transaction row */}
        <div className="form-group">
          <label htmlFor="furnishing">Furnishing</label>
          <select
            id="furnishing"
            name="furnishing"
            value={formData.furnishing}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.furnishing ? 'input-error' : ''}
            required
          >
            <option value="">Select Furnishing</option>
            {sortedFurnishing.map((val) => (
              <option key={val} value={val}>
                {val}
              </option>
            ))}
          </select>
          {errors.furnishing && (
            <span className="error-text" id="error-furnishing">
              {errors.furnishing}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="transaction">Transaction</label>
          <select
            id="transaction"
            name="transaction"
            value={formData.transaction}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.transaction ? 'input-error' : ''}
            required
          >
            <option value="">Select Transaction</option>
            {sortedTransaction.map((val) => (
              <option key={val} value={val}>
                {val}
              </option>
            ))}
          </select>
          {errors.transaction && (
            <span className="error-text" id="error-transaction">
              {errors.transaction}
            </span>
          )}
        </div>

        {/* Ownership & Facing row */}
        <div className="form-group">
          <label htmlFor="ownership">Ownership</label>
          <select
            id="ownership"
            name="ownership"
            value={formData.ownership}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.ownership ? 'input-error' : ''}
            required
          >
            <option value="">Select Ownership</option>
            {sortedOwnership.map((val) => (
              <option key={val} value={val}>
                {val}
              </option>
            ))}
          </select>
          {errors.ownership && (
            <span className="error-text" id="error-ownership">
              {errors.ownership}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="facing">Facing</label>
          <select
            id="facing"
            name="facing"
            value={formData.facing}
            onChange={handleInputChange}
            disabled={loading}
            className={errors.facing ? 'input-error' : ''}
            required
          >
            <option value="">Select Facing</option>
            {sortedFacing.map((val) => (
              <option key={val} value={val}>
                {val}
              </option>
            ))}
          </select>
          {errors.facing && (
            <span className="error-text" id="error-facing">
              {errors.facing}
            </span>
          )}
        </div>
      </div>

      <button type="submit" className="btn-primary" disabled={loading} id="btn-submit-predict">
        {loading ? (
          <>
            <div className="spinner" aria-hidden="true" />
            <span>Predicting...</span>
          </>
        ) : (
          <span>Predict House Price</span>
        )}
      </button>
    </form>
  );
});
