# Lab Guide: Deploying and Demonstrating OpenClaw with Ollama and Local AI Models via Docker

This lab guide demonstrates how to install, configure, and operate a fully containerized **Local AI Agent** stack using **OpenClaw** and **Ollama** via **Docker**. Everything runs 100% locally with zero external cloud API dependencies, featuring **`qwen3:8b`** and **`glm4:9b`** models, and is verified through a live Web UI.

The guide begins with the standard independent deployment flow, followed by an advanced DevOps enhancement that refactors `docker-compose.yml` for unified multi-container orchestration.

> **Acknowledgments & Credit:**  
> This deployment guide is adapted and extended from: [ติดตั้ง OpenClaw ผ่าน Docker](https://yielding-peanut-896.notion.site/OpenClaw-Docker-32d84743c63d801cb0e6e5557607c911).

---

## Overview: Core Component Definitions

- ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) **Docker**: The **"portable container box"** that packages applications and dependencies together so they run consistently anywhere without cluttering or breaking your host system.
- ![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white) **Ollama**: The **"local AI engine"** that loads machine learning model weights into RAM/VRAM and serves fast LLM inference directly on your machine.
- ![Local Model](https://img.shields.io/badge/Local_Model-Weight-4B5563?style=flat-square) **Local AI Model**: The **"digital brain"** (`qwen3:8b` and `glm4:9b`) stored on your local drive—running 100% offline, keeping data completely private, and incurring zero API costs.
- ![OpenClaw](https://img.shields.io/badge/OpenClaw-Framework-E5533D?style=flat-square) **OpenClaw**: The **"AI Agent framework"** that gives the brain a voice and hands—connecting your local models to an intuitive Web UI and empowering them with real-world tool execution (file reading, code execution, web search).

---

## Prerequisites

1. **Docker Desktop (4.x+)**: Installed with WSL2 backend enabled and actively running.
2. **Git**: Installed for cloning the repository.
3. **Hardware Recommendations**:
   - At least 16 GB RAM (32 GB recommended for running 8B/9B models smoothly).
   - 20 GB free disk space (for Docker images and model weights).

---

## Part 1: Standard Step-by-Step Deployment

In this initial phase, we deploy Ollama and OpenClaw following the standard independent setup process.

### Step 1: Run Ollama Container (Local AI Engine)

We begin by provisioning the Local AI engine container:

```powershell
docker run -d `
  --name openclaw-ollama-1 `
  --restart unless-stopped `
  -p 11434:11434 `
  -v ${HOME}/.ollama/models:/root/.ollama/models `
  ollama/ollama:latest
```

Verify that the Ollama container is running and its API responds:
```powershell
docker ps --filter "name=openclaw-ollama-1"
curl http://localhost:11434
```
*Expected output:* `Ollama is running`

---

### Step 2: Download Target Models (`qwen3:8b` & `glm4:9b`) and Verify Inference

Download the two target models into the Ollama container:

```powershell
# 1. Pull Qwen 3 8B
docker exec -it openclaw-ollama-1 ollama pull qwen3:8b

# 2. Pull GLM-4 9B
docker exec -it openclaw-ollama-1 ollama pull glm4:9b
```

Verify installed models:
```powershell
docker exec openclaw-ollama-1 ollama list
```
*Sample output:*
```text
NAME         ID              SIZE      MODIFIED
qwen3:8b     500a1f067a9f    5.2 GB    Just now
glm4:9b      5b699761eca5    5.5 GB    Just now
```

Test inference directly via CLI:
```powershell
docker exec -it openclaw-ollama-1 ollama run qwen3:8b "Hello! Introduce yourself briefly."
```
Once the model responds, press `Ctrl+D` to exit. The Local AI engine and models are verified.

---

### Step 3: Clone OpenClaw and Build Docker Image

Clone the OpenClaw source code and build the local container image:

```powershell
# Clone the repository
git clone https://github.com/openclaw/openclaw.git

# Enter the project directory
cd openclaw

# Build the Docker image
docker build -t openclaw:local -f Dockerfile .
```

---

### Step 4: Configuration & Environment Setup

#### 4.1 Generate Security Token and Create Directories
```powershell
# Generate a 32-byte secure token
[guid]::NewGuid().ToString("N") + [guid]::NewGuid().ToString("N")

# Create local directories
mkdir C:\Users\$env:USERNAME\.openclaw
mkdir C:\Users\$env:USERNAME\.openclaw\workspace
```
> Save your token (e.g., `6fb2bb07f86145609f27b3a44a19692947f37c7b9dbc46c483991951f6ac6b0b`).

#### 4.2 Create the `.env` File
Create `.env` in the root of the `openclaw` repository:

```env
OPENCLAW_CONFIG_DIR=/c/Users/YOUR_USERNAME/.openclaw
OPENCLAW_WORKSPACE_DIR=/c/Users/YOUR_USERNAME/.openclaw/workspace
OPENCLAW_GATEWAY_PORT=18789
OPENCLAW_BRIDGE_PORT=18790
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_TOKEN=YOUR_GENERATED_TOKEN
OPENCLAW_IMAGE=openclaw:local
OPENCLAW_TZ=Asia/Bangkok
```
*(Replace `YOUR_USERNAME` with your Windows username using Unix path format: `/c/Users/...`)*

#### 4.3 Create Initial `openclaw.json`
Create `C:\Users\<YOUR_USERNAME>\.openclaw\openclaw.json` configuring Ollama and both target models:

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789,
    "auth": { 
      "mode": "token", 
      "token": "YOUR_GENERATED_TOKEN" 
    },
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:18789",
        "http://127.0.0.1:18789"
      ]
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen3:8b"
      },
      "models": {
        "ollama/qwen3:8b": {},
        "ollama/glm4:9b": {}
      }
    }
  },
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://host.docker.internal:11434",
        "api": "ollama",
        "models": [
          {
            "id": "qwen3:8b",
            "name": "Qwen 3 8B",
            "contextWindow": 16384
          },
          {
            "id": "glm4:9b",
            "name": "GLM-4 9B",
            "contextWindow": 16384
          }
        ]
      }
    }
  }
}
```

---

### Step 5: Start OpenClaw Gateway Container

Start the OpenClaw Gateway container:

```powershell
docker compose up -d openclaw-gateway
```

Verify that the Gateway is healthy:
```powershell
docker ps --filter "name=openclaw-gateway"
```
*Expected status:* `Up ... (healthy)` on port `18789`.

---

### Step 6: Usage Demonstration via Web UI

#### 6.1 Retrieve Dashboard URL
```powershell
docker exec openclaw-openclaw-gateway-1 node dist/index.js dashboard --no-open
```

Output format:
```text
http://127.0.0.1:18789/#token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 6.2 Connect and Test Inference
1. Paste the URL into your web browser and click **Connect**.
2. Send a test message in the chat box:
   ```text
   Explain the core difference between Docker images and containers.
   ```
3. *(Optional)* Switch models on the fly by typing `/model ollama/glm4:9b`.
4. **DevOps Evidence:** Verify local execution in another terminal:
   ```powershell
   docker exec openclaw-ollama-1 ollama ps
   ```
   The model will appear loaded in local VRAM/RAM, proving 100% offline local computation.

---

## Part 2: DevOps Enhancement: Multi-Container Auto-Start via `docker-compose.yml`

In the standard workflow above, Ollama and OpenClaw were launched independently using separate commands. **In this enhancement step, we modify `docker-compose.yml` so that both containers are automatically started and linked together with a single command.**

### What We Modify in `docker-compose.yml`:
1. **Add `ollama` as a service**: Defines the container, volume mounts, port mappings, and GPU reservations.
2. **Add `depends_on: - ollama` to `openclaw-gateway`**: Instructs Docker Compose to boot and initialize Ollama before starting OpenClaw.
3. **Inject `OLLAMA_API_KEY: ollama-local`**: Ensures seamless authentication inside the Docker network.
4. **Use Docker named volumes**: Replaces host bind mounts with named volumes (`openclaw_config`, `openclaw_workspace`, `openclaw_secrets`).

### The Enhanced `docker-compose.yml` Configuration:

```yaml
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE:-openclaw:local}
    build: .
    env_file:
      - path: .env
        required: false
    environment:
      HOME: /home/node
      OPENCLAW_HOME: /home/node
      TERM: xterm-256color
      OPENCLAW_STATE_DIR: /home/node/.openclaw
      OPENCLAW_CONFIG_PATH: /home/node/.openclaw/openclaw.json
      OPENCLAW_CONFIG_DIR: /home/node/.openclaw
      OPENCLAW_WORKSPACE_DIR: /home/node/.openclaw/workspace
      OPENCLAW_GATEWAY_PORT: "18789"
      OPENCLAW_GATEWAY_TOKEN: ${OPENCLAW_GATEWAY_TOKEN:-}
      OLLAMA_API_KEY: ollama-local
      OPENCLAW_ALLOW_INSECURE_PRIVATE_WS: ${OPENCLAW_ALLOW_INSECURE_PRIVATE_WS:-}
      OPENCLAW_DISABLE_BONJOUR: ${OPENCLAW_DISABLE_BONJOUR:-}
      TZ: ${OPENCLAW_TZ:-UTC}
    depends_on:
      - ollama
    volumes:
      - openclaw_config:/home/node/.openclaw
      - openclaw_workspace:/home/node/.openclaw/workspace
      - openclaw_secrets:/home/node/.config/openclaw
    ports:
      - "${OPENCLAW_GATEWAY_PORT:-18789}:18789"
      - "${OPENCLAW_BRIDGE_PORT:-18790}:18790"
    init: true
    restart: unless-stopped

  openclaw-cli:
    image: ${OPENCLAW_IMAGE:-openclaw:local}
    profiles: ["cli"]
    network_mode: "service:openclaw-gateway"
    env_file:
      - path: .env
        required: false
    volumes:
      - openclaw_config:/home/node/.openclaw
      - openclaw_workspace:/home/node/.openclaw/workspace
      - openclaw_secrets:/home/node/.config/openclaw
    stdin_open: true
    tty: true
    init: true
    entrypoint: ["node", "dist/index.js"]
    depends_on:
      - openclaw-gateway

  ollama:
    image: ollama/ollama:latest
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ~/.ollama/models:/root/.ollama/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  openclaw_config:
  openclaw_workspace:
  openclaw_secrets:
```

### The New One-Command Workflow:
Now, launching the entire environment is reduced to a single command:

```powershell
docker compose up -d
```

Docker Compose automatically evaluates the dependency graph:
1. It spins up `openclaw-ollama-1` first.
2. It launches `openclaw-openclaw-gateway-1` second.
3. Both containers run in the shared Docker network, ready for immediate use.

Verify both are running simultaneously:
```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## Useful DevOps Commands

| Task | Command |
| :--- | :--- |
| View Gateway Logs | `docker logs -f openclaw-openclaw-gateway-1` |
| View Ollama Logs | `docker logs -f openclaw-ollama-1` |
| Monitor Resource Usage | `docker stats openclaw-openclaw-gateway-1 openclaw-ollama-1` |
| Stop All Containers | `docker compose down` |
| Start All Containers | `docker compose up -d` |

---

## References & Acknowledgments

- **Reference / Original Guide**: [ติดตั้ง OpenClaw ผ่าน Docker](https://yielding-peanut-896.notion.site/OpenClaw-Docker-32d84743c63d801cb0e6e5557607c911)
- **OpenClaw Project**: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Ollama Documentation**: [ollama.com](https://ollama.com)

