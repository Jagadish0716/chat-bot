# Jagadish ChatBot (Gemini AI)

A production-ready AI Chatbot built with **Streamlit** and **LangChain**, powered by **Google Gemini Pro**. This project features a fully automated CI/CD pipeline and built-in HTTPS support via Caddy.

## Key Features

* **AI-Powered:** Uses Google's Gemini models for intelligent, context-aware responses.
* **Automatic HTTPS:** Integrated with **Caddy Server** for automatic SSL certificate management.
* **Containerized:** Fully Dockerized for consistent deployment.
* **CI/CD Ready:** Includes a `Jenkinsfile` for automated building, testing, and deployment.
* **Process Management:** Uses **Supervisor** to manage both the Streamlit app and Caddy server within a single container.

## Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLM Framework:** [LangChain](https://www.langchain.com/)
* **AI Model:** Google Gemini
* **Reverse Proxy:** [Caddy](https://caddyserver.com/)
* **Automation:** Jenkins & Docker

## Prerequisites

* A **Google AI (Gemini) API Key**.
* A registered domain name (to use the Caddy HTTPS features).
* **Docker** installed on your server.

## Setup & Installation

### 1. Environment Variables

The application requires a Google API key. You should set this in your environment or Jenkins credentials:

```bash
export GOOGLE_API_KEY='your_gemini_api_key_here'

```

### 2. Configuration

Update the `Caddyfile` with your own domain name to enable automatic SSL:

```caddy
www.your-domain.com {
    reverse_proxy localhost:8501
}

```

### 3. Local Deployment (Docker)

You can build and run the entire stack using Docker:

```bash
# Build the image
docker build -t chatbot-gemini .

# Run the container
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  --name chatbot-container \
  chatbot-gemini

```

## CI/CD Pipeline

The included `Jenkinsfile` automates the entire lifecycle:

1. **Checkout:** Pulls code from GitHub.
2. **Build:** Creates a Docker image tagged with the Git commit hash.
3. **Login/Push:** Securely authenticates and pushes the image to Docker Hub (`jagadish1607/chat-bot`).
4. **Deploy:** Automatically replaces the old container on the production node with the new version.
5. **Notifications:** Sends an email status report (Success/Failure) to the administrator.

## Project Structure

* `app.py`: The core Streamlit application logic and LangChain integration.
* `Dockerfile`: Multi-stage setup for Python, Caddy, and system dependencies.
* `Caddyfile`: Reverse proxy configuration for SSL/HTTPS.
* `supervisord.conf`: Ensures both the web app and the proxy stay running.
* `Jenkinsfile`: Definitive "Pipeline-as-Code" for automated deployments.
* `requirements.txt`: Python dependencies.
