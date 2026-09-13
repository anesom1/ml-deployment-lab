import pandas as pd
import requests
import json
import os


API_URL = "http://localhost:8000/predict" 

# Get the folder where this script is saved
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "sample_batch.csv")

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_path)

# Convert the DataFrame to a JSON string (converting NaN values to standard JSON 'null's),
# then parse that JSON string back into a list of Python dictionaries (one dictionary per row)
json_data = json.loads(df.to_json(orient="records"))

# Iterate through each passenger record in the dataset
for row in json_data:
    # Safely extract the PassengerId to track each request in console output
    passenger_id = row.get("PassengerId")
    
    try:
        # Send a POST request with the row dictionary as a JSON payload, setting a 5-second timeout
        response = requests.post(API_URL, json=row, timeout=5)
        
        # Print the HTTP status code returned by the API (e.g., 200 OK, 400 Bad Request)
        print(f"PassengerId {passenger_id}: Status {response.status_code}")
        
        # Print the response body returned by the API (e.g., prediction result or error message)
        print(f"  Response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        # Catch network errors, connection failures, or timeouts without crashing the loop
        print(f"PassengerId {passenger_id}: ERROR - {e}")
        