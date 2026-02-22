# Use official lightweight Python 3.10 image
FROM python:3.10-slim

LABEL maintainer="Jagadish V" \
      version="1.2" \
      description="Streamlit Chat-bot with Automatic HTTPS via Caddy"

WORKDIR /app

# --------------------------------------------------
# Install System Dependencies & Caddy
# --------------------------------------------------
RUN apt update && apt install -y \
    build-essential \
    curl \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    libgl1 \
    libglib2.0-0 \
    supervisor \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt update && apt install caddy -y \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Python Setup
# --------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose ports for Caddy (HTTP/HTTPS)
EXPOSE 80
EXPOSE 443

# --------------------------------------------------
# Process Management (Supervisord)
# --------------------------------------------------
# Move configs to standard locations
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY Caddyfile /etc/caddy/Caddyfile

# Start Supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]