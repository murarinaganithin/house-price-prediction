import os
import json
import joblib
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.utils.logging_config import logger
from app.api.routes import prediction

def resolve_path(path_str: str) -> str:
    if os.path.isabs(path_str):
        return path_str
    # Resolve relative to the backend directory (grandparent of this file)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.abspath(os.path.join(backend_dir, path_str))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Application startup logic
    logger.info("Application starting up...")
    
    # 1. Resolve paths
    abs_model_path = resolve_path(settings.MODEL_PATH)
    abs_map_path = resolve_path(settings.LOCATION_PRICE_MAP_PATH)
    abs_defaults_path = resolve_path(settings.MODEL_DEFAULTS_PATH)
    abs_options_path = resolve_path(settings.MODEL_OPTIONS_PATH)
    
    logger.info(f"Loading ML model from: {abs_model_path}")
    logger.info(f"Loading location map from: {abs_map_path}")
    logger.info(f"Loading model defaults from: {abs_defaults_path}")
    logger.info(f"Loading model options from: {abs_options_path}")
    
    # 2. Check existence of files
    if not os.path.exists(abs_model_path):
        logger.critical(f"Model file not found at {abs_model_path}. Exiting.")
        raise FileNotFoundError(f"Model file not found at {abs_model_path}")
    if not os.path.exists(abs_map_path):
        logger.critical(f"Location price map not found at {abs_map_path}. Exiting.")
        raise FileNotFoundError(f"Location price map not found at {abs_map_path}")
    if not os.path.exists(abs_defaults_path):
        logger.critical(f"Model defaults not found at {abs_defaults_path}. Exiting.")
        raise FileNotFoundError(f"Model defaults not found at {abs_defaults_path}")
    if not os.path.exists(abs_options_path):
        logger.critical(f"Model options not found at {abs_options_path}. Exiting.")
        raise FileNotFoundError(f"Model options not found at {abs_options_path}")
        
    try:
        # 3. Load artifacts
        app.state.model = joblib.load(abs_model_path)
        logger.info("ML model loaded successfully")
        
        with open(abs_map_path, "r", encoding="utf-8") as f:
            app.state.location_price_map = json.load(f)
        logger.info("Location map loaded successfully")
        
        with open(abs_defaults_path, "r", encoding="utf-8") as f:
            app.state.model_defaults = json.load(f)
        logger.info("Model defaults loaded successfully")
        
        with open(abs_options_path, "r", encoding="utf-8") as f:
            app.state.model_options = json.load(f)
        logger.info("Model options loaded successfully")
        
    except Exception as err:
        logger.critical(f"Startup failed to load ML artifacts: {str(err)}", exc_info=True)
        raise err
        
    yield
    
    # Application shutdown logic
    logger.info("Application shutting down...")
    app.state.model = None
    app.state.location_price_map = None
    app.state.model_defaults = None
    app.state.model_options = None
    logger.info("ML artifacts cleared from state.")

from fastapi.responses import RedirectResponse

# Create FastAPI instance with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.MODEL_VERSION,
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins by default in dev, can be configured via settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(prediction.router, tags=["prediction"])

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


