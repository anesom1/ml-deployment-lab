import pandas as pd
from sklearn.model_selection import train_test_split
from shared.preprocess import build_preprocessor
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import joblib


# Load dataset as dataframe
titanic = pd.read_csv("model/data/titanic.csv")

# Split into features(X) and target(y)
X = titanic.drop('Survived', axis=1)
y = titanic['Survived']

# Split into train and test set
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create preprocessor
preprocessor = build_preprocessor()

# Fit and transform the train set
X_train = preprocessor.fit_transform(X_train)

# Transform test set
X_test = preprocessor.transform(X_test)

# Fit data on the LogisticRegression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Get predictions on the test set
pred = model.predict(X_test)

# Print accuracy on the test set
acc = accuracy_score(y_test, pred)
print("Accuracy: ", acc)

# Save artifacts 
joblib.dump(model, "model/artifacts/model.pkl")
joblib.dump(preprocessor, "model/artifacts/preprocessor.pkl")