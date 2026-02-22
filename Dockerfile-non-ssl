# Use official lightweight Python 3.10 image
FROM python:3.10-slim

LABEL maintainer="Jagadish V" \
      version="1.0" \
      created="2026-02-21" \
      description="Streamlit Chat-bot application"

# Set Working Directory
WORKDIR /app


# --------------------------------------------------
# Install System Dependencies
# --------------------------------------------------
# build-essential  -> Required for compiling some Python packages
# libgl1           -> Required for OpenCV and image processing
# libglib2.0-0     -> Required by many ML libraries
# Remove apt cache to reduce image size
RUN apt update && apt install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy Requirements File First (Better Caching)
COPY requirements.txt .

# Upgrade pip & Install Python Dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copies everything from current directory to container
COPY . .

# Expose Application Port
# Streamlit runs on port 8501 by default
EXPOSE 8501

# --------------------------------------------------
# Run Streamlit Application
# --------------------------------------------------
# --server.address=0.0.0.0 makes app accessible outside container
# Otherwise it binds only to localhost
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]