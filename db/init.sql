CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    input_data JSONB,
    prediction INTEGER,
    probability FLOAT,
    model_version VARCHAR(50)
);