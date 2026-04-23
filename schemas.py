from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

# --- Intent Layer: Why is the caller here? ---
class CallingIntent(BaseModel):
    industry: str = Field("generic", description="e.g., fintech, healthcare, telco")
    workload_type: str = Field("production", pattern="^(production|non-prod|batch)$")
    correlation_id: Optional[str] = None

# --- Constraints Layer: What are the non-functional requirements? ---
class ExecutionConstraints(BaseModel):
    priority: str = Field("balanced", pattern="^(speed|precision|cost-optimized)$")
    max_latency_ms: int = 500
    budget_cap: Optional[float] = None

# --- Request Schema: The Stateless Payload ---
class InferenceRequest(BaseModel):
    intent: CallingIntent
    constraints: ExecutionConstraints
    # Stateless Continuity: The caller provides history for failover/degraded mode
    session_context: Optional[List[Dict[str, str]]] = []
    attributes: Optional[Dict[str, Any]] = {}

# --- Error Schema: Actionable Intelligence ---
class ChalkHillError(BaseModel):
    code: str
    category: str
    message: str
    retryable: bool
    suggested_action: str
    trace_id: str
