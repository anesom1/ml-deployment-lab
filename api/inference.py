import joblib
import pandas as pd
from api.schemas import PassengerInput

# Load artifacts
model = joblib.load("model/artifacts/model.pkl")
preprocessor = joblib.load("model/artifacts/preprocessor.pkl")

# Create function that takes validated input, create DataFrame with training columns and make prediction. Function returns prediction and probability
def predict_passenger(passenger: PassengerInput):
    # Conver Pydantic object into a dictionary
    data = {
        "Pclass": passenger.Pclass,
        "Sex": passenger.Sex,
        "Age": passenger.Age,
        "SibSp": passenger.SibSp,
        "Parch": passenger.Parch,
        "Fare": passenger.Fare,
        "Embarked": passenger.Embarked,
    }

    # Create a one-row DataFrame
    df = pd.DataFrame([data])

    # Apply preprocessor (same used for training)
    X = preprocessor.transform(df)

    # Get prediction
    pred = int(model.predict(X)[0])

    # Get probability of Survived(1)
    prob = float(model.predict_proba(X)[0][1]) # [0] - first/only passenger; [1] - prob for class 1 (Survivded)

    return pred, prob