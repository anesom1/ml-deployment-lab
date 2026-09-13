from typing import Optional
from pydantic import BaseModel, Field

# Define pydantic models for Passender inpit and prediction response
class PassengerInput(BaseModel):
    Age : Optional[float] = Field(default=None, ge=0) # age can be float or none, must greater or equal 0
    Embarked : Optional[str] = Field(default=None)
    Pclass : int = Field(..., ge=1, le=3) # ... field is required, >= 1 & <=3
    Sex : str
    SibSp : int
    Parch : int
    Fare: float

class PredicitonResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str