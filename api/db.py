import os
import logging
import psycopg2
from psycopg2.extras import Json


def get_connection():
    # Connect using environment variables
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )


def insert_prediction(input_data, prediction, probability, model_version):
    try:
        # Open database connection
        conn = get_connection()
        cursor = conn.cursor()

        # Insert prediction into the database
        cursor.execute(
            """
            INSERT INTO predictions
                (input_data, prediction, probability, model_version)
            VALUES
                (%s, %s, %s, %s)
            """,
            (
                Json(input_data),
                prediction,
                probability,
                model_version,
            ),
        )

        # Save the changes
        conn.commit()

        # Close connection
        cursor.close()
        conn.close()

    except Exception as e:
        # Log error but don't stop the API
        logging.error("Failed to log prediction: %s", e)

# If the database goes down, we accept losing some logs rather than making the prediction API unavailable