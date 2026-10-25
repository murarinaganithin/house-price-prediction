import json
import os
import random
from fastapi import APIRouter, Request, HTTPException, status
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.preprocessing import build_model_features
from app.services.inference import InferenceService
from app.utils.logging_config import logger
from app.core.config import settings

router = APIRouter()

# Load seed samples once at module level
_SEED_SAMPLES_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "seed_samples.json"
)
try:
    with open(_SEED_SAMPLES_PATH, "r", encoding="utf-8") as _f:
        _SEED_SAMPLES = json.load(_f)
    logger.info(f"Loaded {len(_SEED_SAMPLES)} seed samples from {_SEED_SAMPLES_PATH}")
except Exception as _e:
    _SEED_SAMPLES = []
    logger.warning(f"Could not load seed samples: {_e}")

@router.get("/health", response_model=dict)
def health_check(request: Request):
    """
    Verify application health and that all ML artifacts are loaded.
    """
    model_loaded = hasattr(request.app.state, "model") and request.app.state.model is not None
    defaults_loaded = hasattr(request.app.state, "model_defaults") and request.app.state.model_defaults is not None
    location_map_loaded = hasattr(request.app.state, "location_price_map") and request.app.state.location_price_map is not None
    
    is_healthy = model_loaded and defaults_loaded and location_map_loaded
    
    if not is_healthy:
        logger.error(
            "Health check failed. Artifacts status: "
            f"model_loaded={model_loaded}, defaults_loaded={defaults_loaded}, location_map_loaded={location_map_loaded}"
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Required ML models or configuration files are not loaded."
        )
        
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_version": settings.MODEL_VERSION
    }

@router.get("/options", response_model=dict)
def get_model_options(request: Request):
    """
    Exposes the categorical choices (furnishing, transaction, ownership, facing, locations) for frontend clients.
    """
    options = getattr(request.app.state, "model_options", None)
    if options is None:
        logger.error("Model options requested but not loaded in application state")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model options configuration is not loaded."
        )
    return options

@router.post("/predict", response_model=PredictionResponse)
def predict_price(request: Request, payload: PredictionRequest):
    """
    Processes property characteristics, engineers model features, and returns the predicted price.
    """
    logger.info("Prediction request received")
    
    # 1. Retrieve model and configurations from app state
    model = getattr(request.app.state, "model", None)
    model_defaults = getattr(request.app.state, "model_defaults", None)
    location_price_map = getattr(request.app.state, "location_price_map", None)
    
    if model is None or model_defaults is None or location_price_map is None:
        logger.error("Inference requested but ML artifacts are not loaded in application state")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model is not ready to serve predictions."
        )
        
    try:
        # 2. Build model features (preprocessing and engineering)
        logger.info(f"Preprocessing input for location: {payload.location}")
        features_df = build_model_features(
            request=payload,
            model_defaults=model_defaults,
            location_price_map=location_price_map
        )
        
        # 3. Call inference service
        inference_service = InferenceService(model=model)
        predicted_val = inference_service.predict(features_df)
        
        logger.info(f"Prediction completed successfully. Predicted Price: {predicted_val}")
        return PredictionResponse(
            predicted_price=predicted_val,
            currency="INR",
            model_version=settings.MODEL_VERSION
        )
        
    except ValueError as val_err:
        logger.error(f"Validation or parsing error in preprocessing: {str(val_err)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err)
        )
    except Exception as err:
        logger.error(f"Unexpected prediction failure: {str(err)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while calculating the prediction."
        )

@router.get("/seed", response_model=dict)
def get_seed_sample():
    """
    Returns a random seed sample for quick-fill testing.
    Each call returns a different sample from the pool.
    """
    if not _SEED_SAMPLES:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No seed samples are available."
        )
    sample = random.choice(_SEED_SAMPLES)
    logger.info(f"Returning seed sample for location: {sample.get('location', 'unknown')}")
    return sample
