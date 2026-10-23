FROM python:3.12-slim

WORKDIR /app

# Install Flask and machine-learning dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and trained model
COPY . .

# Expose Flask API port
EXPOSE 7860

# Start Flask with Gunicorn
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:7860", "app:rental_price_predictor_api"]
