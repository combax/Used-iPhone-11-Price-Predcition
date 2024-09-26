from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import pandas as pd
import numpy as np

# Load the models
price_model = joblib.load("best_price_model.pkl")
shipping_model = joblib.load("best_shipping_model.pkl")

# Load the LabelEncoders
le_condition = joblib.load("le_condition.pkl")
le_location = joblib.load("le_location.pkl")
le_model = joblib.load("le_model.pkl")

# Initialize FastAPI app
app = FastAPI()

# Define request model with more specific field types and validation
class PredictionRequest(BaseModel):
    Condition: Literal['Brand New', 'New (Other)', 'Open Box', 'Excellent - Refurbished', 
                       'Very Good - Refurbished', 'Good - Refurbished', 'Pre-Owned', 'Parts Only']
    Seller_location: str
    Seller_reviews: int = Field(..., ge=0)
    Seller_rating: float = Field(..., ge=0, le=5)
    Storage: Literal['64', '128', '256']
    Carrier_Status: Literal['Locked', 'Unlocked']
    Model: Literal['11', '11 Pro', '11 Pro Max']

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Encode the categorical variables
        condition_encoded = le_condition.transform([request.Condition])[0]
        location_encoded = le_location.transform([request.Seller_location])[0]
        model_encoded = le_model.transform([request.Model])[0]
        
        # Create the input DataFrame
        input_data = pd.DataFrame([[
            condition_encoded,
            location_encoded,
            request.Seller_reviews,
            request.Seller_rating,
            int(request.Storage),
            0 if request.Carrier_Status.lower() == 'locked' else 1,
            model_encoded
        ]], columns=['Condition', 'Seller_location', 'Seller_reviews',
                     'Seller_rating', 'Storage', 'Carrier_Status', 'Model'])
        
        # Predict the price and shipping
        predicted_price = price_model.predict(input_data)[0]
        predicted_shipping = shipping_model.predict(input_data)[0]
        
        return {
            "predicted_price": round(float(predicted_price), 2),
            "predicted_shipping": round(float(predicted_shipping), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the iPhone Price and Shipping Prediction API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)