# Local AI Agent Orchestration & LLM Benchmark Lab

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![OpenClaw](https://img.shields.io/badge/OpenClaw-E5533D?style=for-the-badge&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

A comprehensive DevOps and Local AI laboratory project demonstrating the end-to-end containerized deployment of an autonomous AI Agent framework (**OpenClaw**) integrated with a private **Ollama** LLM inference engine. 

The project operates **100% locally and offline** with zero reliance on paid third-party cloud APIs. Additionally, it features an empirical benchmarking suite comparing code generation and game logic implementation between **Qwen 3 (8B)** and **GLM-4 (9B)**.

---

## Table of Contents

- [Overview & Key Highlights](#overview--key-highlights)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [LLM Benchmark: Qwen 3 (8B) vs. GLM-4 (9B)](#llm-benchmark-qwen-3-8b-vs-glm-4-9b)
- [Quick Start Guide](#quick-start-guide)
  - [1. Running the Local AI Stack (Docker Compose)](#1-running-the-local-ai-stack-docker-compose)
  - [2. Running the Python Benchmark Games](#2-running-the-python-benchmark-games)
- [DevOps Design Decisions](#devops-design-decisions)
- [Useful Commands](#useful-commands)
- [References & Acknowledgments](#references--acknowledgments)
- [License](#license)

---

## Overview & Key Highlights

- **Multi-Container Orchestration**: Manages both OpenClaw Gateway and the Ollama LLM engine inside a unified `docker-compose.yml` stack using service dependency rules (`depends_on`).
- **Complete Privacy & Cost Control**: Inferences run locally on GPU/CPU with no data leakage or per-token API costs.
- **Persistent Model Storage**: Dedicated Docker volume management ensures model weights (`qwen3:8b`, `glm4:9b`) persist across container restarts.
- **Empirical Code Generation Benchmark**: Analyzes how open-weights models approach state management, collision algorithms, and GUI rendering in Python.

---

## System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                              Host Machine                              │
│                                                                        │
│   ┌─────────────────────┐             ┌────────────────────────────┐   │
│   │   Browser (User)    │             │       Docker Engine        │   │
│   └──────────┬──────────┘             └──────────────┬─────────────┘   │
│              │ (Port 18789)                          │                 │
│              ▼                                       ▼                 │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Container: openclaw-openclaw-gateway-1                         │   │
│   │ - Agent Execution & Tool Calling Engine                        │   │
│   │ - Serves Web Control UI Dashboard                              │   │
│   └──────────────────────────────┬─────────────────────────────────┘   │
│                                  │ (Shared Docker Bridge Network)      │
│                                  ▼                                     │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Container: openclaw-ollama-1                                   │   │
│   │ - Local LLM Inference Daemon (Port 11434)                      │   │
│   │ - Volume: ~/.ollama/models:/root/.ollama/models                │   │
│   └──────────────────────────────┬─────────────────────────────────┘   │
│                                  ▼                                     │
│                     ┌────────────────────────┐                         │
│                     │ Model Weights (Local)  │                         │
│                     │ - qwen3:8b (5.2 GB)    │                         │
│                     │ - glm4:9b (5.5 GB)     │                         │
│                     └────────────────────────┘                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```text
devops/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow (Docker & Python tests)
├── docker-compose.yml         # Multi-container orchestration definition
├── .env.example               # Template for environment variables and secrets
├── openclaw.json.example      # Template for OpenClaw gateway & model registration
├── .gitignore                 # Excludes virtual environments, caches, and secrets
├── LICENSE                    # MIT open-source license
├── README.md                  # Project landing page and architectural documentation
├── DOCKER_OLLAMA_GUIDE.md     # Step-by-step technical deployment manual
├── result.md                  # Comparative benchmark evaluation report
├── requirements.txt           # Unified Python dependencies (pygame-ce)
│
├── Model1-GLM/                # Model 1 Implementation (GLM-4 9B)
│   ├── main.py                # Snake game implementation using Pygame
│   └── requirements.txt       # Pygame-ce dependency
│
└── Model2-QWEN/               # Model 2 Implementation (Qwen 3 8B)
    ├── main.py                # Snake game implementation using Tkinter
    └── requirements.txt       # Standard library documentation
```

---

## LLM Benchmark: Qwen 3 (8B) vs. GLM-4 (9B)

Both models were independently prompted with the exact same natural language specification:

> **Benchmark Prompt:**  
> `"สร้างเกมงู (Snake Game) ด้วย Python พร้อมหน้าจอ GUI และปุ่มเริ่มเกม"`  
> *(English: "Create a Snake Game using Python with a GUI window and a game start button.")*

Below is the comparative evaluation based on core game mechanics and architectural choices from [result.md](result.md):


| Evaluation Criteria       | Model 1: GLM-4 (9B)                               | Model 2: Qwen 3 (8B)                                    |
| ------------------------- | ------------------------------------------------- | ------------------------------------------------------- |
| **GUI Framework**         | `Pygame`                                          | `Tkinter` (Standard Library)                            |
| **Body Movement**         | Appends new head to list, tracks delta offsets    | Calculates next position, inserts at head index         |
| **Reverse Prevention**    | Checks proposed direction against opposite vector | Enforces direction lock before movement turn            |
| **Self-Collision Logic**  | Iterates through body segments excluding head     | Checks if predicted head coordinate exists in body list |
| **Smart Food Spawning**   | Re-rolls food coordinate if overlapping body list | Re-rolls food coordinate if overlapping body list       |
| **External Dependencies** | Requires `pygame-ce`                              | Zero external dependencies (runs out of the box)        |


Detailed analysis and code snippets are available in [result.md](result.md).

---

## Quick Start Guide

### 1. Running the Local AI Stack (Docker Compose)

Ensure **Docker Desktop** is running, then execute:

```powershell
# 1. Copy the environment configuration
Copy-Item .env.example .env

# 2. Launch both Ollama and OpenClaw services simultaneously
docker compose up -d

# 3. Pull the target models into the Ollama container
docker exec -it openclaw-ollama-1 ollama pull qwen3:8b
docker exec -it openclaw-ollama-1 ollama pull glm4:9b

# 4. Retrieve the authenticated Web UI dashboard URL
docker exec openclaw-openclaw-gateway-1 node dist/index.js dashboard --no-open
```

Open the generated tokenized URL in your browser and click **Connect** to access the Control UI.

For the comprehensive, step-by-step setup walkthrough, see [DOCKER_OLLAMA_GUIDE.md](DOCKER_OLLAMA_GUIDE.md).

---

### 2. Running the Python Benchmark Games

```powershell
# 1. Create and activate a Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the GLM-4 implementation (Pygame)
python Model1-GLM/main.py

# 4. Run the Qwen 3 implementation (Tkinter)
python Model2-QWEN/main.py
```

---

## DevOps Design Decisions

1. **Service Decoupling**: Decoupled the LLM inference engine (Ollama) from the agent orchestration layer (OpenClaw) into isolated containers. If the Agent Gateway crashes or restarts, loaded model memory in Ollama remains intact.
2. **Infrastructure as Code (IaC)**: Configured the entire multi-service lifecycle inside `docker-compose.yml`, reducing cluster startup to a single `docker compose up -d` command.
3. **Compatibility-Engineered Dependencies**: Standardized on `pygame-ce` across `requirements.txt` to guarantee cross-compatibility across modern Python versions (3.11 – 3.14+) on Windows, Linux, and macOS.
4. **Security by Default**: Enforces token-based gateway authentication and isolates container networks to prevent unauthorized remote code execution.

---

## Useful Commands


| Task                         | Command                                                          |
| ---------------------------- | ---------------------------------------------------------------- |
| Check Container Status       | `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` |
| Check Loaded LLM Models      | `docker exec openclaw-ollama-1 ollama ps`                        |
| Stream OpenClaw Gateway Logs | `docker logs -f openclaw-openclaw-gateway-1`                     |
| Stream Ollama Engine Logs    | `docker logs -f openclaw-ollama-1`                               |
| Stop Entire Stack            | `docker compose down`                                            |


---

## References & Acknowledgments

- **Reference / Original Deployment Guide**: [ติดตั้ง OpenClaw ผ่าน Docker](https://yielding-peanut-896.notion.site/OpenClaw-Docker-32d84743c63d801cb0e6e5557607c911)
- **OpenClaw Project**: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Ollama Project**: [ollama.com](https://ollama.com)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.