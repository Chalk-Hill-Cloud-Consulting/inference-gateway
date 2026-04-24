from .schemas import InferenceRequest

class ProtocolMarshaller:
    @staticmethod
    def to_gemini(request: InferenceRequest) -> dict:
        contents = []
        for msg in request.session_context:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        return {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": request.constraints.max_output_tokens,
                "temperature": 0.7
            }
        }

    @staticmethod
    def to_openai(request: InferenceRequest) -> dict:
        return {
            "model": request.model_alias or "gpt-4o-mini",
            "messages": request.session_context,
            "max_tokens": request.constraints.max_output_tokens
        }

    @staticmethod
    def to_claude(request: InferenceRequest) -> dict:
        system = next((m["content"] for m in request.session_context if m["role"] == "system"), "")
        messages = [m for m in request.session_context if m["role"] != "system"]
        return {
            "model": request.model_alias or "claude-3-5-sonnet-latest",
            "system": system,
            "messages": messages,
            "max_tokens": request.constraints.max_output_tokens
        }
