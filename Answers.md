## Milestone 5:

1. Which rows produced a prediction, and which were rejected by Pydantic? Why the difference?

All rows poduced predictions. We made sure that Age and Embarked is optional. 

2. What did your pipeline do with the unknown port "X"? Trace it back to a specific line in preprocess.py.

It hits OneHotEncoder(handle_unknown="ignore") line in preprocess.py. Because "X" was never seen in training, the encoder produces an all-zero vector for the Embarked columns instead of erroring. Prediction proceeds, but the model is effectively predicting as if it has no information about embarkation port for that row.

3. What did "Male" do? If it did not behave the way you expected, that is a real finding — how would you fix it, and in which file does the fix belong?

OneHotEncoder does exact string matching. "Male" ≠ "male", so it is treated as an unseen category — same as "X" above — and silently zeroed out, not mapped to the male column. The fix belongs either in schemas.py (normalize/lowercase the input, or validate against an enum(the value must be exactly one of the two listed options)) or as an explicit normalization step added to the preprocessing pipeline itself.

4. Is a prediction on a row with missing age as trustworthy as one on a complete row? Your API returns both with equal confidence. Should it?

No, the API returns a probability with equal confidence for both, but a row with an imputed median age carries more uncertainty than a row with a real observed age. The API currently has no way to communicate that. As a fix we could flag imputed-field predictions (e.g., an "imputed_fields" list in the response).


## Reflection questions:
1. Explain training/serving skew in your own words, and name the specific design decision in this lab that prevents it. 

When the preprocessing applied to inputs at the prediction time differs from what was applied at the training time the model sees data shaped differently from what it learned on. That will lead lower accuracy and with no error thrown. 
The design decision preventing it here is shared preprocesser: one module, imported by both train.py and the API.

2. Why is the fitted preprocessor saved as a separate artifact instead of being rebuilt in the API at startup?

build_preprocessor() only defines the steps; the actual fitted values (e.g median age, scale factors, category mappings) only exist after fitting on the training data. Rebuilding it in the API would need the training CSV (that is not in the image) and could produce different values — that would reintroduce skew.

3. Your API logs to Postgres but does not fail when Postgres is down. Describe one scenario where that is the right choice and one where it is dangerous.

Right choice: If the API predicts Titanic survival for users, they should still receive a prediction even if the logging database is temporarily unavailable. Logging is helpful, but making predictions is the main purpose of the API, so it is better to continue serving users.

Dangerous: It is dangerous in systems where every prediction must be recorded, such as medical diagnoses or banking fraud detection. If the database is down, losing those records could make auditing, investigations, or legal compliance impossible.

4. Your prediction log table is the beginning of a monitoring system. What else would you need to log to detect that your model's accuracy is degrading in production?

- The true outcome (ground truth) when it becomes available later, so I can compare predictions with the real result and calculate accuracy over time.
- Prediction probability (confidence) to see if the model becomes less confident.
- Input feature distributions (such as Age, Fare, and Embarked) to detect data drift when production data looks different from the training data.
- Model version to compare the performance of different deployed models.
- Prediction timestamp to identify when performance started to change.


5. You retrain the model next month on newer data. Which files change, and what breaks if you forget to redeploy the preprocessor alongside the model?

model/train.py runs again, producing new model.pkl and a new preprocessor.pkl — both must be regenerated together, since the preprocessor's fitted values (medians, scales, categories) are tied to that specific training run. If we redeploy only the new model.pkl and forget the new preprocessor.pkl, we get the skew: the model expects data scaled/encoded one way, but it's receiving data transformed by the old preprocessor — silent, hard-to-diagnose degraded predictions with no error.