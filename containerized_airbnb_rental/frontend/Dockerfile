FROM python:3.12-slim

WORKDIR /app

# Install frontend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit application
COPY . .

# Streamlit application port
EXPOSE 8501

# Launch Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
