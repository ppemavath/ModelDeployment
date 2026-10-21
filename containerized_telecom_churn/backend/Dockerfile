FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask application and model
COPY . .

EXPOSE 7860

# Start Flask through Gunicorn
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:7860", "app:app"]
