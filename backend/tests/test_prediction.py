import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert "model_version" in data

def test_get_options(client):
    response = client.get("/options")
    assert response.status_code == 200
    data = response.json()
    assert "locations" in data
    assert "furnishing" in data
    assert "transaction" in data
    assert "ownership" in data
    assert "facing" in data
    assert "bangalore" in data["locations"]
    assert "Furnished" in data["furnishing"]

def test_valid_prediction(client):
    payload = {
        "location": "Whitefield",
        "carpet_area": 1200,
        "bathroom": 2.0,
        "balcony": 2.0,
        "floor": "5 out of 10",
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert data["predicted_price"] > 0
    assert data["currency"] == "INR"
    assert data["model_version"] == "1.0"

def test_invalid_carpet_area(client):
    payload = {
        "location": "Whitefield",
        "carpet_area": -50.0,  # Invalid: <= 0
        "bathroom": 2.0,
        "balcony": 2.0,
        "floor": "5 out of 10",
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_invalid_bathroom(client):
    payload = {
        "location": "Whitefield",
        "carpet_area": 1200.0,
        "bathroom": 0.0,  # Invalid: <= 0
        "balcony": 2.0,
        "floor": "5 out of 10",
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_invalid_balcony(client):
    payload = {
        "location": "Whitefield",
        "carpet_area": 1200.0,
        "bathroom": 2.0,
        "balcony": -1.0,  # Invalid: < 0
        "floor": "5 out of 10",
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_empty_categorical_field(client):
    payload = {
        "location": "   ",  # Invalid: whitespace only
        "carpet_area": 1200.0,
        "bathroom": 2.0,
        "balcony": 2.0,
        "floor": "5 out of 10",
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_unknown_location(client):
    payload = {
        "location": "unseen-random-location-name",  # Unknown location
        "carpet_area": 1200.0,
        "bathroom": 2.0,
        "balcony": 2.0,
        "floor": "5 out of 10",
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert data["predicted_price"] > 0

@pytest.mark.parametrize("floor_input", [
    "Ground",
    "Upper Basement",
    "Lower Basement",
    "5 out of 10",
    "  Ground  ",
    "12 out of 12"
])
def test_special_floors_valid(client, floor_input):
    payload = {
        "location": "Whitefield",
        "carpet_area": 1200.0,
        "bathroom": 2.0,
        "balcony": 2.0,
        "floor": floor_input,
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] > 0

def test_malformed_floor(client):
    payload = {
        "location": "Whitefield",
        "carpet_area": 1200.0,
        "bathroom": 2.0,
        "balcony": 2.0,
        "floor": "not-a-floor-string",  # Malformed floor format
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    assert "Malformed floor value" in response.json()["detail"]
