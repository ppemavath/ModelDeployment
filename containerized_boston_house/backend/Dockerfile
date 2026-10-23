FROM python:3.12-slim

WORKDIR /app

# Copy and install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask application and trained model
COPY . .

# Flask API port
EXPOSE 7860

# Run Flask using Gunicorn
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:7860", "app:app"]
