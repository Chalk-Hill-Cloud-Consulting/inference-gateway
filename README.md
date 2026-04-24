# Chalk Hill Neural Gateway

A stateless, intent-aware API Gateway designed for **Governed AI Inference**. This reference architecture solves the "Deprecation Trap" of modern LLM providers by providing a resilient, vendor-agnostic abstraction layer for high-availability production environments.

## 🏗️ Architecture & Operational Principles

The **Chalk Hill Neural Gateway** is built on the principle of **Stateless Continuity**. By delegating session history to the payload and utilizing in-memory semantic caching, the infrastructure remains horizontally scalable and immune to the "stickiness" or brittleness of backend provider states.

### **Core Capabilities:**
* **Omni-Protocol Marshalling:** Native "Shim" layers for Google (Gemini), OpenAI (GPT/Llama), and Anthropic (Claude), translating a unified internal contract into provider-specific REST dialects.
* **Active Resilience & Failover:** Automated intercept of 429 (Throttling) and 503 (Unavailable) errors with integrated exponential backoff and node-rotation logic.
* **FinOps Governance:** Cost-aware scheduling that routes traffic based on `workload_type` (Dev vs. Prod) and explicit `max_output_tokens` ceilings.
* **Infrastructure-Lite Semantic Caching:** In-memory FAISS-based vector caching that bypasses LLM inference for redundant queries—reducing latency to <10ms for cached hits.
* **Contract-First Governance:** Enforces strict execution constraints (latency, priority) via Pydantic V2 validated schemas.

## 🛠️ Tech Stack
* **Language:** Python 3.12+
* **Framework:** FastAPI (Asynchronous Transport Layer)
* **Validation:** Pydantic V2 & Pydantic-Settings
* **Resilience:** HTTPX (Async I/O) with custom Backoff logic
* **Caching:** In-memory Semantic Vector Index

## 🚀 Getting Started

### 1. Environment Configuration
Create a `.env` file in the root directory. This gateway uses **Runtime URI Derivation**, allowing you to update endpoints without a code rebuild.

```env
# API Keys
GOOGLE_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# URI Templates (Dynamic Derivation)
GEMINI_URI_TEMPLATE=[https://generativelanguage.googleapis.com/v1beta/models/$](https://generativelanguage.googleapis.com/v1beta/models/$){model_id}:generateContent?key=${api_key}
OPENAI_URI_TEMPLATE=[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)
CLAUDE_URI_TEMPLATE=[https://api.anthropic.com/v1/messages](https://api.anthropic.com/v1/messages)
```

## 2. Installation & Execution
```
# Install dependencies
pip install -r requirements.txt

# Start the Gateway
uvicorn app.main:app --reload
```

## 📂 Repository Structure
```
inference-gateway/
├── app/
│   ├── main.py              # FastAPI Entry Point
│   ├── schemas.py           # Pydantic Governance Layer
│   ├── services.py          # Resilience & Cache Engine
│   ├── marshaller.py        # Protocol Translation (The "Shim")
│   └── config.py            # Runtime URI Derivation
├── .env                     # Injected Environment (Git Ignored)
└── README.md                # Architectural Documentation
```


© 2026 Chalk Hill Cloud Consulting LLC. All rights reserved.
Licensed under the MIT License.

