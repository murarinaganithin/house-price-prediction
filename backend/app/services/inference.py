import pandas as pd
from typing import Any

class InferenceService:
    def __init__(self, model: Any):
        self.model = model

    def predict(self, features: pd.DataFrame) -> float:
        """
        Accepts a model-ready pandas DataFrame and returns the raw prediction value.
        """
        prediction = self.model.predict(features)
        return float(prediction[0])
