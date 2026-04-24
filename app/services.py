import httpx
import asyncio
import logging
from string import Template
from typing import Dict, Any, Optional

from .schemas import InferenceRequest
from .marshaller import ProtocolMarshaller
from .config import settings

# Configure logging for Chalk Hill operational visibility
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChalkHillGateway")

class InferenceEngine:
    def __init__(self):
        self.client = httpx.AsyncClient()
        # In-memory semantic cache placeholder
        # For 'Gold Master', this uses the raw query as the key
        self.cache: Dict[str, str] = {}

    def _derive_url(self, model_id: str) -> str:
        """Constructs the provider endpoint at runtime using URI templates."""
        if "gemini" in model_id:
            return Template(settings.gemini_uri_template).substitute(
                model_id=model_id, api_key=settings.google_api_key
            )
        if "claude" in model_id:
            return settings.claude_uri_template
        
        # Default to OpenAI-compatible endpoints (GPT, Llama)
        return settings.openai_uri_template

    async def execute(self, request: InferenceRequest) -> Dict[str, Any]:
        # 1. Semantic Cache Check
        last_message = request.session_context[-1]["content"]
        if last_message in self.cache:
            logger.info(f"Cache Hit for query: {last_message[:30]}...")
            return {"source": "cache", "content": self.cache[last_message]}

        # 2. Dynamic Routing & Resilience Loop
        # Fallback sequence: Primary -> Secondary (Failover)
        model_id = request.model_alias or getattr(settings, "gemini_model_id", "gemini-1.5-flash")
        
        for attempt in range(3):
            try:
                url = self._derive_url(model_id)
                payload = self._marshall(request, model_id)
                headers = self._get_headers(model_id)
                
                # Enforce Latency Constraint as an HTTPX timeout
                timeout_sec = request.constraints.max_latency_ms / 1000.0
                
                response = await self.client.post(
                    url, json=payload, headers=headers, timeout=timeout_sec
                )

                # Handle Throttling (429) with Exponential Backoff
                if response.status_code == 429:
                    wait_time = 2 ** attempt
                    logger.warning(f"Throttled (429). Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()
                
                # Normalize provider-specific output (simplified for reference)
                content = self._extract_content(data, model_id)
                
                # Update Cache & Return
                self.cache[last_message] = content
                return {
                    "source": "inference",
                    "model": model_id,
                    "content": content,
                    "correlation_id": request.intent.correlation_id
                }

            except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                # Pivot to a fallback model on final attempt or error
                model_id = "gpt-4o-mini" if "gemini" in model_id else "gemini-2.5-flash"
                continue

        raise Exception("Resilience Engine Exhausted: All backend nodes failed.")

    def _marshall(self, request: InferenceRequest, model_id: str) -> Dict[str, Any]:
        if "gemini" in model_id: return ProtocolMarshaller.to_gemini(request)
        if "claude" in model_id: return ProtocolMarshaller.to_claude(request)
        return ProtocolMarshaller.to_openai(request)

    def _get_headers(self, model_id: str) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if "gpt" in model_id or "llama" in model_id:
            headers["Authorization"] = f"Bearer {settings.openai_api_key}"
        elif "claude" in model_id:
            headers.update({
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01"
            })
        return headers

    def _extract_content(self, data: Dict[str, Any], model_id: str) -> str:
        """Normalizes disparate provider response shapes into a single string."""
        try:
            if "gemini" in model_id:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            if "claude" in model_id:
                return data["content"][0]["text"]
            # Default OpenAI/Llama shape
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "Error: Unexpected provider response shape."
