# Chat Bot

Simple chat-bot project with Docker and Jenkins deployment support.

**Contents**
- **Overview:** quick summary and features
- **Prerequisites:** what you need locally
- **Install & Run:** local and Docker instructions
- **Deployment:** Jenkins and Caddy notes
- **Config files:** where to look

## Overview

This repository contains a Python-based chat-bot application. The main entrypoint is `app.py`. The project is prepared to run locally, in Docker, or in CI/CD via the included `Jenkinsfile`.

## Features

- Minimal chat-bot service (Python)
- Dockerized for easy deployment
- Reverse proxy support via `Caddyfile`
- Supervisor process configuration via `supervisord.conf`

## Prerequisites

- Python 3.8+ (if running locally)
- Docker (to run the container)
- Git (to clone the repo)

## Quickstart — Local (virtualenv)

1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
python app.py
```

The app should start on the configured host/port (see `app.py`).

## Docker

Build the image:

```bash
docker build -t chat-bot:latest -f Dockerfile .
```

Run the container:

```bash
docker run -d --name chat-bot -p 8000:8000 chat-bot:latest
```

If you prefer the non-SSL Dockerfile, use `Dockerfile-non-ssl` when building.

## Jenkins / CI

The repository includes a `Jenkinsfile` for CI/CD pipelines. Adjust pipeline steps as needed for your Jenkins setup (credentials, agents, and Docker hosts).

There are helper scripts in `bash-scripts/`:

- `bash-scripts/install_docker.sh` — install Docker on a host
- `bash-scripts/install_jenkins.sh` — provision Jenkins

## Reverse Proxy (Caddy)

The `Caddyfile` is provided as an example to terminate TLS and proxy requests to the chat-bot service. Update domain names and paths to match your environment.

## Supervisor

`supervisord.conf` contains an example supervisor configuration to run the application as a managed service in a container or VM.

## Configuration

- `requirements.txt` — Python dependencies
- `app.py` — application entrypoint and config
- `Jenkinsfile` — CI/CD pipeline

## Troubleshooting

- Check logs from the container: `docker logs chat-bot`
- For supervisor issues, check `/var/log/supervisor/` inside the container or host

## Contributing

Feel free to open issues and pull requests. Keep changes small and focused; document behavior changes in the PR description.

## License

Specify license here (e.g., MIT) or add a `LICENSE` file.

---

If you'd like, I can expand any section (configuration examples, env vars, or a sample Jenkins pipeline stage). Tell me which parts to elaborate.
