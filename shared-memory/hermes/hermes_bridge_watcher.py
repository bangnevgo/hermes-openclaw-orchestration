#!/usr/bin/env python3
"""
Hermes Bridge Watcher - Versi AI-Team
Monitor incoming/request.json dari AI-Team workspace
dan forward ke Hermes CLI, tulis response ke outgoing/response_nerve_req.json
"""

import json
import subprocess
import time
import hashlib
from pathlib import Path

# PATH BARU: Mengarah ke AI-Team
INCOMING = Path.home() / "AI-Team/shared-memory/hermes/incoming/request.json"
OUTGOING = Path.home() / "AI-Team/shared-memory/hermes/outgoing/response_nerve_req.json"
POLL_INTERVAL = 2
last_hash = None


def file_hash(path):
    try:
        return hashlib.md5(path.read_bytes()).hexdigest()
    except Exception:
        return None


def call_hermes(message: str) -> str:
    try:
        result = subprocess.run(
            ["hermes", "chat", "-Q", "-q", message],
            capture_output=True,
            text=True,
            timeout=120,
        )
        response = result.stdout.strip()
        if not response:
            response = result.stderr.strip() or "No response from Hermes."
        # Strip UI border dan session_id line
        lines = response.splitlines()
        clean = [l for l in lines if not l.startswith("╭") and not l.startswith("╰") and not l.startswith("session_id:")]
        return "\n".join(clean).strip()
    except subprocess.TimeoutExpired:
        return "Hermes timeout."
    except Exception as e:
        return f"Error calling Hermes: {e}"


def process_request():
    global last_hash
    if not INCOMING.exists():
        return

    current_hash = file_hash(INCOMING)
    if current_hash == last_hash:
        return

    last_hash = current_hash

    try:
        data = json.loads(INCOMING.read_text())
        message = data.get("payload", {}).get("message", "")
        request_id = data.get("request_id", "unknown")

        if not message:
            return

        print(f"[bridge] Request [{request_id}]: {message[:80]}")
        response_text = call_hermes(message)
        print(f"[bridge] Response: {response_text[:80]}")

        OUTGOING.parent.mkdir(parents=True, exist_ok=True)
        OUTGOING.write_text(json.dumps({
            "request_id": request_id,
            "status": "ok",
            "message": response_text
        }, ensure_ascii=False, indent=2))

        print(f"[bridge] Written to {OUTGOING}")

    except Exception as e:
        print(f"[bridge] Error: {e}")


def main():
    print(f"[bridge] Watching {INCOMING}")
    print(f"[bridge] Output to {OUTGOING}")
    while True:
        process_request()
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
