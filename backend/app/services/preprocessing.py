import re
import pandas as pd
from typing import Tuple, Dict, Any
from app.schemas.prediction import PredictionRequest

def parse_floor(floor_str: str) -> Tuple[int, int]:
    s = floor_str.strip().lower()
    if s == "ground":
        return 0, 1
    elif s == "upper basement":
        return -1, 1
    elif s == "lower basement":
        return -2, 1
    
    # Match "X out of Y"
    match = re.match(r"^(\d+)\s+out\s+of\s+(\d+)$", s)
    if match:
        n_floor = int(match.group(1))
        total_floor = int(match.group(2))
        if total_floor == 0:
            total_floor = 1
        return n_floor, total_floor
        
    raise ValueError(f"Malformed floor value: '{floor_str}'")

def normalize_location(location_str: str) -> str:
    # Convert to lower case, strip, replace spaces with hyphens
    return location_str.strip().lower().replace(" ", "-")

def build_model_features(
    request: PredictionRequest,
    model_defaults: Dict[str, Any],
    location_price_map: Dict[str, float]
) -> pd.DataFrame:
    # 1. Parse floor
    n_floor, total_floor = parse_floor(request.floor)
    
    # 2. Normalize location and resolve location price
    norm_location = normalize_location(request.location)
    if norm_location in location_price_map:
        avg_location_price = location_price_map[norm_location]
        location_feature = norm_location
    else:
        avg_location_price = model_defaults.get("overall_median_price", 7500000.0)
        location_feature = "other"
        
    # 3. Calculate derived features
    floor_ratio = n_floor / (total_floor if total_floor != 0 else 1)
    is_ground_floor = 1 if n_floor == 0 else 0
    is_top_floor = 1 if n_floor == total_floor else 0
    total_amenities = request.bathroom + request.balcony
    bath_to_balcony_ratio = request.bathroom / (request.balcony + 1.0)
    
    # 4. Construct feature dictionary matching the exact expected order of model.feature_names_in_
    # feature_names_in_: ['location', 'carpet_area', 'transaction', 'furnishing', 'facing', 'bathroom', 
    #                     'balcony', 'ownership', 'n_floor', 'total_floor', 'avg_location_price', 
    #                     'floor_ratio', 'is_ground_floor', 'is_top_floor', 'total_amenities', 
    #                     'bath_to_balcony_ratio']
    features = {
        "location": location_feature,
        "carpet_area": request.carpet_area,
        "transaction": request.transaction,
        "furnishing": request.furnishing,
        "facing": request.facing,
        "bathroom": request.bathroom,
        "balcony": request.balcony,
        "ownership": request.ownership,
        "n_floor": float(n_floor),
        "total_floor": float(total_floor),
        "avg_location_price": float(avg_location_price),
        "floor_ratio": float(floor_ratio),
        "is_ground_floor": int(is_ground_floor),
        "is_top_floor": int(is_top_floor),
        "total_amenities": float(total_amenities),
        "bath_to_balcony_ratio": float(bath_to_balcony_ratio)
    }
    
    # Create DataFrame (1 row)
    df = pd.DataFrame([features])
    return df
