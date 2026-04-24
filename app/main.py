from fastapi import FastAPI, HTTPException
from .schemas import InferenceRequest
from .services import InferenceEngine

# The entry point for the Chalk Hill Neural Gateway
app = FastAPI(
    title="Chalk Hill Neural Gateway",
    description="A stateless, resilient AI inference gateway.",
    version="1.0.0"
)

# Initialize the engine once at startup
engine = InferenceEngine()

@app.get("/")
async def root():
    return {"status": "online", "gateway": "Chalk Hill Neural Gateway"}

@app.post("/v1/inference")
async def process_inference(request: InferenceRequest):
    try:
        # The core orchestration happens here
        result = await engine.execute(request)
        return result
    except Exception as e:
        # Map internal errors to a professional 503 Service Unavailable
        raise HTTPException(status_code=503, detail=str(e))
