# HermesOPC-Nerve-Bridge

Integrasi **Hermes Agent (CLI)** ke dalam **Nerve UI (OpenClaw)** menggunakan arsitektur file-based bridge.

## Arsitektur
Nerve UI → OpenClaw Agent → incoming/request.json → Bridge Service → Hermes CLI → outgoing/response.json → OpenClaw Agent → Nerve UI
OpenClaw agent dikonfigurasi via SOUL.md untuk bertindak sebagai jembatan murni — tidak menjawab sendiri, hanya relay ke Hermes.

## Struktur File
AI-Team/
├── shared-memory/hermes/
│   ├── bridge_service.py          # Core bridge: polling incoming, call Hermes CLI
│   ├── hermes_bridge.py           # Versi alternatif bridge
│   ├── hermes_bridge_watcher.py   # Watcher variant
│   ├── hermes_watcher.py          # Watcher variant
│   ├── SOUL.md                    # Instruksi untuk OpenClaw agent
│   ├── IDENTITY.md                # Identitas agent
│   ├── AGENTS.md                  # Daftar agent
│   ├── BOOTSTRAP.md               # Bootstrap instructions
│   ├── HEARTBEAT.md               # Heartbeat config
│   ├── TOOLS.md                   # Tool definitions
│   ├── USER.md                    # User context
│   ├── incoming/                  # Request masuk dari Nerve UI
│   ├── outgoing/                  # Response dari Hermes
│   └── memory/                    # Persistent memory Hermes


## Cara Kerja

1. User kirim pesan di Nerve UI
2. OpenClaw agent (via SOUL.md) tulis `incoming/request.json`
3. `bridge_service.py` polling setiap 2 detik, deteksi file baru via MD5 hash
4. Bridge panggil `hermes chat -Q -q "pesan"` via subprocess
5. Response ditulis ke `outgoing/response_nerve_req.json`
6. OpenClaw agent baca response dan tampilkan ke user

## Menjalankan Bridge

```bash
pm2 start ~/AI-Team/shared-memory/hermes/bridge_service.py --name hermes-bridge --interpreter python3
pm2 save
```

## Requirements

- OpenClaw + Nerve UI
- Hermes Agent CLI (`hermes` tersedia di PATH)
- Python 3
- PM2

## Author

Bang Nding — Nevgo Institute
