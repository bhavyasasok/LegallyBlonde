FROM python:3.11-slim

# Install build essentials and Fortran compiler for SciPy
RUN apt-get update \
    && apt-get install -y \
       build-essential \
       gfortran \
       libopenblas-dev \
       liblapack-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port (adjust if needed)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
