# Titanic Survival Prediction API

This project is a small end-to-end machine learning deployment example that trains a Titanic survival model, exposes it through a FastAPI service, and stores prediction logs in PostgreSQL.

It demonstrates a common production workflow:

- train and save a model
- package the app with Docker
- serve predictions via a REST API
- persist requests and predictions in a database
- test the service with example payloads

## Overview

The application predicts whether a passenger survived the Titanic disaster based on fields such as class, sex, age, fare, family size, and embarkation port.

The model is trained with scikit-learn using a logistic regression classifier, and the preprocessing pipeline is saved alongside the model so inference behaves consistently with training.

## Architecture

- `api/` contains the FastAPI application and inference logic
- `model/` contains the training script and saved model artifacts
- `shared/` contains the preprocessing pipeline used by inference
- `db/` contains the database initialization script
- `new_examples/` contains sample data and scripts to exercise the API
- `docker-compose.yml` runs the API, PostgreSQL database, and Adminer UI

## Project Structure

```text
ml-deployment-lab/
├── api/
│   ├── db.py
│   ├── Dockerfile
│   ├── inference.py
│   ├── main.py
│   ├── requirements.txt
│   └── schemas.py
├── db/
│   └── init.sql
├── model/
│   ├── artifacts/
│   ├── data/
│   │   └── titanic.csv
│   └── train.py
├── new_examples/
│   ├── create_sample_data.py
│   ├── post_row.py
│   └── sample_batch.csv
├── shared/
│   └── preprocess.py
├── docker-compose.yml
├── README.md
└── .env.example
```

## Prerequisites

Before running the project, make sure you have:

- Docker
- Docker Compose
- Python 3.10+ (for local model training and testing)
- pip

## Environment Variables

Create a `.env` file in the project root with values like:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=titanic
```

These values are used by Docker Compose to configure PostgreSQL and the API container.

## Training the Model

From the project root:

```bash
cd ml-deployment-lab
python model/train.py
```

This script:

- loads the Titanic dataset
- splits the data into train/test sets
- builds a preprocessing pipeline
- fits a logistic regression model
- saves artifacts to `model/artifacts/`

Artifacts created:

- `model/artifacts/model.pkl`
- `model/artifacts/preprocessor.pkl`

## Running the API with Docker

Start the full stack:

```bash
docker compose up --build
```

This brings up:

- FastAPI app on `http://localhost:8000`
- PostgreSQL database on the internal Docker network
- Adminer at `http://localhost:8080` for database inspection

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Example response:

```json
{"status": "ok"}
```

### Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Pclass": 3,
    "Sex": "male",
    "Age": 22,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 7.25,
    "Embarked": "S"
  }'
```

Example response:

```json
{
  "prediction": 0,
  "probability": 0.42,
  "model_version": "1.0.0"
}
```

### Request Schema

The API accepts a JSON payload with the following fields:

- `Pclass`: integer from 1 to 3
- `Sex`: string, typically `male` or `female`
- `Age`: optional float or null
- `SibSp`: integer
- `Parch`: integer
- `Fare`: float
- `Embarked`: optional string

## Database Logging

Each prediction is stored in the `predictions` table created by `db/init.sql`.

Columns:

- `id`
- `created_at`
- `input_data` (JSONB)
- `prediction`
- `probability`
- `model_version`

This makes it easy to audit model requests and outputs over time.

## Example Scripts

The repository includes scripts for testing the API with realistic payloads.

### Create sample data

```bash
python new_examples/create_sample_data.py
```

This produces a CSV file with example rows including edge cases such as missing age, invalid port values, and different fare values.

### Post batch data to the API

```bash
python new_examples/post_row.py
```

This script reads the sample CSV and sends each row to the `/predict` endpoint.

## Development Notes

The core inference path is:

`PassengerInput -> validation -> preprocessing -> model -> prediction/probability -> response`

The training and inference code use the same preprocessing configuration so the pipeline remains consistent between model development and production use.

## Typical Workflow

1. Create environment variables in `.env`
2. Train the model with `python model/train.py`
3. Run the stack with `docker compose up --build`
4. Send requests to the API
5. Inspect results in PostgreSQL or Adminer


