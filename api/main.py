from fastapi import FastAPI
from api.schemas import PassengerInput, PredicitonResponse
from api.inference import predict_passenger
from api.db import insert_prediction

app = FastAPI() 

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredicitonResponse)
def predict(passenger: PassengerInput):
        pred, prob = predict_passenger(passenger)

        insert_prediction(
        input_data=passenger.model_dump(),
        prediction=pred,
        probability=prob,
        model_version="1.0.0",
        )
        
        return PredicitonResponse(
              prediction=pred,
              probability=prob,
              model_version="1.0.0"
        )

# flow: PassengerInput -> Pydantic validation -> predict_passenger() -> preprocessor ->
# -> logisticRegression model -> prob, pred -> Prediction Response -> Json response