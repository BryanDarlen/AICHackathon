from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
ENV_FILE = ROOT / ".env"


def load_env(path: Path) -> None:
    if not path.exists():
        raise SystemExit("Missing .env file. Copy .env.example to .env and add your Chutes values.")

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


def masked(value: str) -> str:
    if len(value) <= 12:
        return "***"
    return f"{value[:6]}...{value[-4:]}"


def main() -> int:
    sys.path.insert(0, str(BACKEND))
    load_env(ENV_FILE)

    required = ["LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        print(f"Chutes test failed: missing {', '.join(missing)} in .env")
        return 1

    if os.getenv("LLM_API_KEY", "").lower().startswith("replace"):
        print("Chutes test failed: LLM_API_KEY still looks like a placeholder.")
        return 1

    # Force live inference for this test only. This does not edit .env.
    os.environ["DEMO_MODE"] = "false"

    print("Testing Chutes/OpenAI-compatible LLM adapter...")
    print(f"Base URL: {os.getenv('LLM_BASE_URL')}")
    print(f"Model: {os.getenv('LLM_MODEL')}")
    print(f"API key: {masked(os.getenv('LLM_API_KEY', ''))}")

    from app.llm_client import LLMUnavailable, chat_json

    try:
        result = chat_json(
            "Return valid JSON only. Do not include markdown.",
            'Return exactly {"ok": true, "provider": "chutes", "task": "reconpilot-test"}',
        )
    except LLMUnavailable as exc:
        print("Chutes test failed.")
        print(f"Reason: {exc}")
        return 1

    if result.get("ok") is True:
        print("Chutes test passed.")
        print(f"Response: {result}")
        return 0

    print("Chutes responded, but not with the expected JSON.")
    print(f"Response: {result}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
