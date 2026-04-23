import asyncio
from schemas import InferenceRequest

class InferenceService:
    async def execute(self, request: InferenceRequest):
        """
        Orchestrates the call with built-in resilience.
        Attempts Primary Model -> Failover/Degraded Mode -> Standardized Error.
        """
        try:
            # 1. Attempt Primary High-Precision Dispatch
            return await self._dispatch_to_node("primary-ultra-node", request)
        
        except Exception as e:
            # 2. THE BRAINS: Interpret the error
            if self._is_retryable(e):
                # Self-Heal: Switch to Degraded Mode (Lower Precision, Higher Availability)
                print(f"Primary failed. Switching to Degraded Mode for {request.intent.industry}...")
                return await self._dispatch_to_node("degraded-fast-node", request)
            
            raise e # If fatal, bubble up to main.py handler

    async def _dispatch_to_node(self, node_id: str, request: InferenceRequest):
        # Simulated Network IO / Inference Call
        # In degraded mode, we would inject the 'session_context' here 
        # to ensure the backup model has the state.
        await asyncio.sleep(0.05) 
        
        return {
            "node_id": node_id,
            "governance_status": "verified",
            "payload": f"Success response using {request.constraints.priority} constraints."
        }

    def _is_retryable(self, e):
        # Logic to determine if we should trigger Degraded Mode
        return True # Simplification for mock
