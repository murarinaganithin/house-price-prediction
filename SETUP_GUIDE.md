# Setup Guide

This guide explains how to set up the project from a fresh clone and run both the backend and frontend correctly.

The project is split into two parts:

- Backend: Python + FastAPI + ML model
- Frontend: React + TypeScript + Vite

Both must be running together for the app to work properly.

---

## 1. Prerequisites

Before starting, make sure these tools are installed on your machine:

- Python 3.10 or newer
- Node.js 18 or newer
- npm
- Git
- A terminal such as PowerShell, CMD, or Git Bash

Check your versions:

```bash
python --version
node --version
npm --version
```

If any command fails, install the missing tool first.

---

## 2. Clone the Repository

```bash
git clone <your-repository-url>
cd "House Price Prediction"
```

After cloning, make sure the project structure looks like this:

```text
House Price Prediction/
├── backend/
├── frontend/
├── docs/
├── README.md
├── SETUP_GUIDE.md
├── .gitignore
└── .venv/   # optional local environment
```

---

## 3. Quick Start Summary

If you want the shortest working flow, do this in order:

1. Create backend virtual environment
2. Install backend packages
3. Add `.env` and trained model file
4. Start backend
5. Install frontend packages
6. Add frontend `.env`
7. Start frontend
8. Open the app in browser

---

## 4. Backend Setup

### Step 1: Go to the backend folder

```bash
cd backend
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### Step 4: Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Create the backend environment file

Copy the example file:

```bash
copy .env.example .env
```

If your system does not support `copy`, create `.env` manually.

Required content:

```env
MODEL_PATH=models/house_price_production_rf.pkl
LOCATION_PRICE_MAP_PATH=models/location_price_map.json
MODEL_DEFAULTS_PATH=models/model_defaults.json
MODEL_OPTIONS_PATH=models/model_options.json
MODEL_VERSION=1.0
APP_NAME="House Price Prediction API"
LOG_LEVEL=INFO
```

### Step 6: Add the trained model file

The model is not committed to Git because it is large, so you must add it manually.

Place the trained model here:

```text
backend/models/house_price_production_rf.pkl
```

This file is required for the backend to start properly.

### Step 7: Start the backend

From the `backend` folder:

```bash
python run.py
```

Or use Uvicorn directly:

```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

The backend should be available at:

- http://localhost:8000
- Swagger docs: http://localhost:8000/docs

---

## 5. Frontend Setup

Open a second terminal window.

### Step 1: Go to the frontend folder

```bash
cd frontend
```

### Step 2: Install dependencies

```bash
npm install
```

### Step 3: Create the frontend environment file

```bash
copy .env.example .env
```

The file should contain:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Step 4: Start the frontend

```bash
npm run dev
```

The frontend will run at:

- http://localhost:5173

---

## 6. Environment Variables

### Backend variables

Create `backend/.env` using the example file.

| Variable | Default | Description |
| --- | --- | --- |
| `MODEL_PATH` | `models/house_price_production_rf.pkl` | Path to the trained ML model |
| `LOCATION_PRICE_MAP_PATH` | `models/location_price_map.json` | Location pricing map used in inference |
| `MODEL_DEFAULTS_PATH` | `models/model_defaults.json` | Default values used during feature engineering |
| `MODEL_OPTIONS_PATH` | `models/model_options.json` | Dropdown choices for frontend form fields |
| `MODEL_VERSION` | `1.0` | Application/model version |
| `APP_NAME` | `House Price Prediction API` | API title shown by FastAPI |
| `LOG_LEVEL` | `INFO` | Logging level |

### Frontend variables

Create `frontend/.env` with:

| Variable | Default | Description |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `http://localhost:8000` | Base URL for backend requests |

---

## 7. API Reference

The backend exposes the following endpoints.

### 7.1 Health check

```bash
curl http://localhost:8000/health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0"
}
```

### 7.2 Get dropdown options

```bash
curl http://localhost:8000/options
```

### 7.3 Get random seed sample

```bash
curl http://localhost:8000/seed
```

### 7.4 Predict price

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Whitefield",
    "carpet_area": 1200,
    "bathroom": 2,
    "balcony": 2,
    "floor": "5 out of 10",
    "furnishing": "Semi-Furnished",
    "transaction": "Resale",
    "ownership": "Freehold",
    "facing": "East"
  }'
```

Example response:

```json
{
  "predicted_price": 8545419.51,
  "currency": "INR",
  "model_version": "1.0"
}
```

---

## 8. Model Training Notebook

If you want to retrain or reproduce the model yourself, use the notebook here:

```text
docs/Notebook/house-price-cleaning-eda-modeling.ipynb
```

This notebook contains the data cleaning, EDA, and model-training workflow used in the project.

---

## 9. Troubleshooting

### Backend does not start

Check the following:

- `backend/.env` exists
- model file exists at `backend/models/house_price_production_rf.pkl`
- dependencies were installed with `pip install -r requirements.txt`
- you activated the correct virtual environment

### Frontend cannot connect to backend

Check:

- backend is running on port 8000
- `frontend/.env` contains `VITE_API_BASE_URL=http://localhost:8000`
- no CORS issue is blocking requests

### Missing model artifact

The app expects the trained model to be generated locally and saved inside `backend/models/`.

---

## 10. Large File Note

The trained model file is large, so it is intentionally not tracked in Git.

If you want to push it to remote Git storage later, use Git LFS:

```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
```

---

## 11. Final Verification

After setup is complete, verify the project is working:

1. Backend is running at http://localhost:8000
2. Frontend is running at http://localhost:5173
3. Swagger docs open at http://localhost:8000/docs
4. You can submit a property and receive a prediction from the frontend

If all four steps work, the setup is complete.
