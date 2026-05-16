import os
import re
import time
import uuid
from typing import Optional


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _now_iso_z() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _append_run_log(line: str) -> None:
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, "run.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line.rstrip("\n") + "\n")


def _build_messages(user_prompt: str, system_prompt: Optional[str]) -> list[dict]:
    sp = (system_prompt or "").strip()
    if not sp:
        sp = "You are a helpful assistant. Be concise and correct."
    return [
        {"role": "system", "content": sp},
        {"role": "user", "content": user_prompt},
    ]


def _postprocess_text(text: str) -> str:
    out = (text or "").strip()
    out = re.sub(r"\s+\n", "\n", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def _redact_secrets(s: str) -> str:
    if not s:
        return s
    s = re.sub(r"sk-[A-Za-z0-9]{16,}", "sk-REDACTED", s)
    s = re.sub(r"Bearer\s+[A-Za-z0-9._-]{12,}", "Bearer REDACTED", s, flags=re.IGNORECASE)
    return s


def call_llm(prompt: str, api_key: str = "", system_prompt: Optional[str] = None) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("prompt is empty")
    if not api_key or not api_key.strip():
        raise ValueError("api_key is missing (expected env var OPENAI_API_KEY)")

    request_id = uuid.uuid4().hex[:6]
    _append_run_log(f"{_now_iso_z()} INFO start request_id={request_id}")
    t0 = time.time()

    try:
        from openai import OpenAI
    except Exception as e:
        raise RuntimeError(
            "openai python package is not available. Install it with `pip install openai`."
        ) from e

    client = OpenAI(api_key=api_key.strip())

    messages = _build_messages(prompt, system_prompt)

    try:
        resp = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=0.2,
        )
    except Exception as e:
        raise RuntimeError(f"OpenAI request failed: {str(e)}") from e

    text = ""
    try:
        text = resp.choices[0].message.content or ""
    except Exception:
        text = ""
    latency_ms = int((time.time() - t0) * 1000)
    _append_run_log(
        f"{_now_iso_z()} INFO success request_id={request_id} api_key={_redact_secrets(api_key.strip())} latency_ms={latency_ms}"
    )
    return _postprocess_text(text)


if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY", "")
    system_prompt = os.getenv("SYSTEM_PROMPT", "You are a careful assistant.")
    print(call_llm("hello", api_key, system_prompt=system_prompt))