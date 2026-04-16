#!/usr/bin/env python3
import json
import subprocess
import time
import hashlib
import sys
from pathlib import Path

# Force unbuffered output
sys.stdout = sys.stderr

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
        print(f"[Bridge] Memanggil Hermes CLI: {message}")
        result = subprocess.run(
            ["hermes", "chat", "-Q", "-q", message],
            capture_output=True,
            text=True,
            timeout=120,
        )
        response = result.stdout.strip()
        if not response:
            response = result.stderr.strip() or "No response from Hermes."
        
        lines = response.splitlines()
        clean = [l for l in lines if not l.startswith("╭") and not l.startswith("╰") and not l.startswith("session_id:")]
        return "\n".join(clean).strip()
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
        
        print(f"==============================")
        print(f"Request Diterima: {message}")
        
        response_text = call_hermes(message)
        
        OUTGOING.parent.mkdir(parents=True, exist_ok=True)
        OUTGOING.write_text(json.dumps({
            "request_id": request_id,
            "status": "ok",
            "message": response_text
        }, ensure_ascii=False, indent=2))
        
        print(f"Respons Terkirim: {response_text[:50]}...")
        
    except Exception as e:
        print(f"ERROR: {e}")

def main():
    print("⚕️ Bridge Service Aktif...")
    print(f"Monitoring: {INCOMING}")
    while True:
        process_request()
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
