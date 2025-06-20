# Dockerfile

FROM python:3.11

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app code
COPY . .

# Expose port for Uvicorn
EXPOSE 8080

# Run FastAPI app (note: app.main is module path, app is FastAPI instance)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
