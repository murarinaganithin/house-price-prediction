from pydantic import BaseModel, Field, field_validator

class PredictionRequest(BaseModel):
    location: str
    carpet_area: float
    bathroom: float
    balcony: float
    floor: str
    furnishing: str
    transaction: str
    ownership: str
    facing: str

    @field_validator('location', 'floor', 'furnishing', 'transaction', 'ownership', 'facing')
    @classmethod
    def validate_non_empty_strings(cls, v: str, info) -> str:
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty or whitespace-only")
        return v

    @field_validator('carpet_area')
    @classmethod
    def validate_carpet_area(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("carpet_area must be greater than zero")
        return v

    @field_validator('bathroom')
    @classmethod
    def validate_bathroom(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("bathroom must be greater than zero")
        return v

    @field_validator('balcony')
    @classmethod
    def validate_balcony(cls, v: float) -> float:
        if v < 0:
            raise ValueError("balcony must be greater than or equal to zero")
        return v


class PredictionResponse(BaseModel):
    predicted_price: float
    currency: str = "INR"
    model_version: str
