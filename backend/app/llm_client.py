from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class LLMUnavailable(RuntimeError):
    pass


def demo_mode_enabled() -> bool:
    return os.getenv("DEMO_MODE", "true").lower() in {"1", "true", "yes", "on"}


def chat_json(system_prompt: str, user_prompt: str) -> dict:
    """Small OpenAI-compatible JSON chat helper.

    The app does not depend on an SDK so Chutes/OpenAI-style providers can be
    swapped by changing environment variables.
    """
    if demo_mode_enabled():
        raise LLMUnavailable("DEMO_MODE is enabled")

    base_url = os.getenv("LLM_BASE_URL", "").rstrip("/")
    api_key = os.getenv("LLM_API_KEY", "")
    model = os.getenv("LLM_MODEL", "")
    if not base_url or not api_key or not model:
        raise LLMUnavailable("LLM_BASE_URL, LLM_API_KEY, or LLM_MODEL is missing")

    payload = {
        "model": model,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = str(exc)
        raise LLMUnavailable(f"HTTP {exc.code}: {detail[:300]}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise LLMUnavailable(str(exc)) from exc

    content = body["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise LLMUnavailable(f"LLM did not return JSON: {content[:160]}") from exc
