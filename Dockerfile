FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy language model using pip (more reliable than spacy download)
RUN pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Copy application code
COPY *.py ./

# Create directories for data and output
RUN mkdir -p /app/data /app/output

# Make the CLI script executable
RUN chmod +x generate_draft.py

# Run the CLI application (one-time draft generation)
CMD ["python3", "generate_draft.py"]

