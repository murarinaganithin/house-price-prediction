# House Price Prediction API Backend

This is the FastAPI backend application for the House Price Prediction model. It wraps a trained Random Forest model and its preprocessing artifacts to provide a high-performance REST API.

## Features

- **Input Validation**: Fast validation of raw user inputs using Pydantic.
- **Derived Feature Engineering**: Automated calculation of floor ratios, floor flags, total amenities, bathroom-to-balcony ratios, and location-level target medians.
- **Robust Fallback**: Automatic fallback to median pricing for unknown locations.
- **Lifespan Management**: One-time model loading at application startup to minimize prediction latency.
- **Detailed Logging**: Structured console logs for request tracing.

---

## Getting Started

### 1. Requirements
Ensure Python 3.10+ is installed.

### 2. Setup and Installation
Navigate to the `backend/` directory and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Verify that the `.env` file exists in the `backend/` folder (or copy it from `.env.example`). The defaults are:
```env
MODEL_PATH=models/house_price_production_rf.pkl
LOCATION_PRICE_MAP_PATH=models/location_price_map.json
MODEL_DEFAULTS_PATH=models/model_defaults.json
MODEL_VERSION=1.0
APP_NAME="House Price Prediction API"
LOG_LEVEL=INFO
```

---

## Running the API Server

Start the application with Uvicorn:
```bash
# From within the backend/ folder:
PYTHONPATH=. uvicorn app.main:app --reload
```

Alternatively, from the workspace root folder:
```bash
$env:PYTHONPATH="backend"; uvicorn app.main:app --reload
```

Once running, the interactive documentation is available at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### 1. Health Check
`GET /health`
Verifies that the server is active and that all serialized machine learning models and defaults are loaded.

**Example Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0"
}
```

### 2. Predict Price
`POST /predict`
Performs feature engineering and regression inference to output a predicted house price.

**Request Payload:**
```json
{
  "location": "Whitefield",
  "carpet_area": 1200,
  "bathroom": 2,
  "balcony": 2,
  "floor": "5 out of 10",
  "furnishing": "Semi-Furnished",
  "transaction": "Resale",
  "ownership": "Freehold",
  "facing": "East"
}
```

**Response:**
```json
{
  "predicted_price": 8545419.51,
  "currency": "INR",
  "model_version": "1.0"
}
```

---

## Running the Test Suite

Execute the tests using pytest:
```bash
# From workspace root:
$env:PYTHONPATH="backend"; pytest backend/tests/
```
