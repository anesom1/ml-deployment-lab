# Use Python 3.11 slim image as the base.
# Slim images are smaller and contain only essential packages.
FROM python:3.11-slim

# Set the working directory inside the container to /app.
# All subsequent commands will run relative to this directory.
WORKDIR /app
# Copy the requirements file into the container.
# This is done before copying the rest of the application to leverage
# Docker's layer caching — if only app code changes, the pip install
# layer is reused from cache.
COPY api/requirements.txt .
# Install all Python dependencies from requirements.txt.
# --no-cache-dir: Prevents pip from storing cache, reducing image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container.
COPY api/ api/
COPY shared/ shared/
COPY model/artifacts/ model/artifacts/

# Expose port 8000
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]