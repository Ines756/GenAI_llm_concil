"""Ollama API client for making LLM requests."""

import time
from backend.metrics import update_metric
import httpx
from typing import List, Dict, Any, Optional
from .config import *


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 500.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Ollama API.

    Args:
        model: Ollama model identifier (e.g., "gemma2:2b", "llama3.2:latest")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds (default 300s = 5 minutes)

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }

    start_time = time.perf_counter()
    success = False

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OLLAMA_ENDPOINTS[model] + OLLAMA_API_PATH,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            success = True

            data = response.json()

            # Vérifier que la génération est complète
            if not data.get('done', False): 
                print(f"Warning: Model {model} response not complete")

            message = data.get('message', {})

            return {
                'content': message.get('content', ''),
                'reasoning_details': None
            }

    except httpx.ReadTimeout:
        print(f"❌ Timeout querying model {model} after {timeout}s")
        print(f"   URL: {OLLAMA_ENDPOINTS[model] + OLLAMA_API_PATH}")
        print(f"   This usually means:")
        print(f"   - Ollama server is not running (start with 'ollama serve')")
        print(f"   - Model '{model}' is not downloaded (run 'ollama pull {model}')")
        print(f"   - Model is taking too long to respond (increase timeout)")
        return None
    except httpx.ConnectError:
        print(f"❌ Cannot connect to Ollama server for {model}")
        print(f"   URL: {OLLAMA_ENDPOINTS[model] + OLLAMA_API_PATH}")
        print(f"   Make sure Ollama is running: 'ollama serve'")
        return None
    except Exception as e:
        print(f"❌ Error querying model {model}: {e}")
        print(f"   URL: {OLLAMA_ENDPOINTS[model] + OLLAMA_API_PATH}")
        print(f"   Payload: {payload}")
        import traceback
        traceback.print_exc()  # Affiche la stack trace complète
        return None
    finally:
        # --- Enregistrement des métriques ---
        latency = time.perf_counter() - start_time
        update_metric(model, latency, success)


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of OpenRouter model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
