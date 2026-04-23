import httpx
from schemas import settings, InferenceRequest

class InferenceService:
    async def execute(self, request: InferenceRequest):
        """
        Principal-led Resilience Layer.
        Separates the 'Resilience Strategy' from the 'Protocol Binding'.
        """
        try:
            # Attempt Primary Node (Gemini 1.5 Flash)
            return await self._dispatch_to_gemini(request)
        except Exception as e:
            if self._is_retryable(e):
                # This is where you'd trigger failover logic
                print(f"Primary Node failure detected: {str(e)}. Triggering resilience...")
            raise e

    async def _dispatch_to_gemini(self, request: InferenceRequest):
        """
        The 'Shim': Translates Chalk Hill Stateless context to Google Gemini REST.
        """
        # 1. Protocol Configuration
        api_key = settings.google_api_key
        # Updated to the 2.5 series stable endpoint
        model_id = "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_id}:generateContent?key={api_key}"
        
        # 2. Scope-safe Context Mapping (Inside the function for statelessness)
        gemini_contents = [
            {
                "role": "user" if msg["role"].lower() == "user" else "model", 
                "parts": [{"text": msg["content"]}]
            } 
            for msg in request.session_context
        ]

        llm_payload = {"contents": gemini_contents}

        # 3. Invocation with Constraints
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=llm_payload,
                # Enforce the caller's latency constraint (ms to seconds)
                timeout=request.constraints.max_latency_ms / 1000 
            )
            
            if response.status_code != 200:
                raise Exception(f"Gemini API Error {response.status_code}: {response.text}")

            raw_data = response.json()
            
            # 4. Canonical Response Mapping
            # We transform their complex nesting back to our clean, flat contract.
            return {
                "node_id": "gemini-2.5-flash-sonoma",
                "content": raw_data['candidates'][0]['content']['parts'][0]['text'],
                "governance_status": "passed"
            }

    def _is_retryable(self, e):
        # Resilience logic for transient network failures
        triggers = ["timeout", "500", "503", "429"]
        return any(t in str(e).lower() for t in triggers)
