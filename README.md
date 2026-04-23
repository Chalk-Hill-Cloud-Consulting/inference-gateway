# Chalk Hill Neural Gateway

A stateless, intent-aware API Gateway designed for governed AI inference. This project serves as a reference architecture for integrating large language models (LLMs) into high-latency or remote infrastructure environments (e.g., rural telco monitoring).

## 🏗 Architecture & Design Principles

Unlike traditional stateful AI integrations, this gateway is built on **Stateless Continuity**. By delegating session history to the payload, the infrastructure remains lightweight, horizontally scalable, and resilient to backend provider failures.

### Key Features:
* **Intent-Based Routing:** Uses structured `CallingIntent` to steer inference toward specific domain-expertise nodes.
* **Engineering Governance:** Enforces strict execution constraints (latency, priority) via Pydantic-validated contracts.
* **Protocol Resilience:** Implements a "Shim" pattern to abstract vendor-specific REST protocols (Gemini, OpenAI, etc.) into a unified Chalk Hill standard.
* **Self-Documenting API:** Built on FastAPI with auto-generated OpenAPI/Swagger UI documentation.

## 🛠 Tech Stack
* **Language:** Python 3.12+
* **Framework:** FastAPI (Asynchronous Transport Layer)
* **Validation:** Pydantic V2 & Pydantic-Settings
* **HTTP Client:** HTTPX (Async Protocol Binding)
* **Inference:** Google Gemini 1.5/2.5/3.0 (via REST)

## 🚀 Getting Started

### 1. Environment Setup
Create a `.env` file in the root directory (this is ignored by Git for security):
```text
GOOGLE_API_KEY=your_secret_key_here



Installation
pip install -r requirements.txt

Running the Gateway
uvicorn main:app --reload


Navigate to http://127.0.0.1:8000/docs to access the interactive Swagger UI.


==============================================================================================================

