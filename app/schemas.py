from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CallingIntent(BaseModel):
    industry: str
    workload_type: str  # e.g., "production", "dev", "batch"
    correlation_id: str

class ExecutionConstraints(BaseModel):
    max_latency_ms: int = Field(default=5000, ge=100)
    priority: str = "balanced"  # "performance", "cost", "balanced"
    max_output_tokens: Optional[int] = 512

class InferenceRequest(BaseModel):
    intent: CallingIntent
    model_alias: Optional[str] = None
    constraints: ExecutionConstraints
    session_context: List[Dict[str, str]]
