# Multi-stage Production Container for Zarya Digital Bank AI Gateway
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8000 \
    APP_ENV=production

# Install essential build and networking tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code and models
COPY . /app/

# Expose FastAPI Gateway (8000) and Streamlit Dashboard (8501)
EXPOSE 8000 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default launch command: starts both FastAPI gateway and Streamlit UI via supervisor/script
CMD ["sh", "-c", "uvicorn deployment_cost_analysis_and_presentation.api_server:app --host 0.0.0.0 --port 8000 & streamlit run deployment_cost_analysis_and_presentation/app.py --server.port 8501 --server.address 0.0.0.0"]

