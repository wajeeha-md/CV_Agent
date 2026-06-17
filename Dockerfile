FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer-cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project
COPY . .

# Expose the port Railway will map to
EXPOSE 8080

# Run Streamlit
CMD ["python", "-m", "streamlit", "run", "src/app.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
