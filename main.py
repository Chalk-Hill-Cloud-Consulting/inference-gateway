from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import JSONResponse
from schemas import InferenceRequest, ChalkHillError
from services import InferenceService

app = FastAPI(title="Chalk Hill Neural Gateway", version="1.1.0")
inference_service = InferenceService()

# --- Global Resilience Handler ---
@app.exception_handler(Exception)
async def governance_exception_handler(request: Request, exc: Exception):
    """
    Ensures that even catastrophic failures return actionable intelligence.
    """
    error = ChalkHillError(
        code="GATEWAY_RESILIENCE_TRIGGERED",
        category="INFRASTRUCTURE",
        message=str(exc),
        retryable=True,
        suggested_action="RETRY_WITH_CONTEXT_TOKEN",
        trace_id=request.headers.get("x-correlation-id", "system-generated")
    )
    return JSONResponse(status_code=502, content=error.dict())

# --- The Principal Endpoint ---
@app.post("/v1/infer")
async def infer(
    payload: InferenceRequest, 
    x_governance_token: str = Header(...)
):
    """
    The main entrance for all inference. 
    Captures intent, enforces constraints, and ensures stateless continuity.
    """
    # The 'Transport' layer delegates to the 'Service' layer
    result = await inference_service.execute(payload)
    
    return {
        "entity": "Chalk Hill Cloud Consulting LLC",
        "result": result,
        "contract_status": "compliant"
    }

@app.get("/health")
async def health():
    return {"status": "operational", "region": "us-west-north-sonoma"}

@app.get("/")
async def welcome():
    return {
        "message": "Chalk Hill Neural Gateway",
        "version": "1.1.0",
        "docs_url": "/docs",
        "health_check": "/health"
    }
