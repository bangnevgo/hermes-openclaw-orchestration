#!/usr/bin/env python3
"""
Hermes Bridge Script (Fixed Version)
Menghubungkan Nerve UI dengan Ekosistem Hermes.
"""

import json
import os
import time
import uuid
import subprocess
from datetime import datetime
from pathlib import Path

# --- Konfigurasi Path ---
BASE_DIR = Path("/home/bangnevgo/AI-Team/shared-memory/hermes")
INCOMING_DIR = BASE_DIR / "incoming"
OUTGOING_DIR = BASE_DIR / "outgoing"
LOG_FILE = BASE_DIR / "bridge.log"

# Pastikan folder ada
INCOMING_DIR.mkdir(parents=True, exist_ok=True)
OUTGOING_DIR.mkdir(parents=True, exist_ok=True)

# --- Fungsi Utilitas ---
def log(message):
    """Log dengan timestamp ke console dan file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + "\n")
    except:
        pass

def get_hermes_response(prompt):
    """
    Mencoba mendapatkan respons dari Hermes.
    Prioritas: 
    1. Hermes CLI (jika terinstall)
    2. Fallback simulasi (jika CLI tidak ada)
    """
    # Cek apakah perintah 'hermes' tersedia di sistem
    try:
        # Menggunakan hermes cli jika ada (sesuaikan perintahnya jika berbeda)
        # Contoh: hermes chat "prompt"
        result = subprocess.run(
            ['hermes', 'chat', '--prompt', prompt], 
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        log("Info: Hermes CLI tidak ditemukan, menggunakan mode simulasi.")
    except subprocess.TimeoutExpired:
        return "Maaf, Hermes membutuhkan waktu terlalu lama untuk merespons."
    except Exception as e:
        log(f"Error subprocess: {e}")

    # --- Fallback Simulation ---
    # Ini akan digunakan jika Hermes CLI tidak ada.
    # Anda bisa mengganti ini dengan logika lain jika diperlukan.
    time.sleep(0.5)
    return (
        f"⚕️ **Hermes Bridge Active**\n\n"
        f"Saya menerima pesan: '{prompt}'\n\n"
        f"*(Mode Simulasi - Hermes CLI tidak terdeteksi. "
        f"Untuk respons penuh, pastikan Hermes Agent berjalan atau CLI terkonfigurasi dengan benar)*"
    )

# --- Logic Utama ---
def process_request(request_file):
    try:
        # Baca file request
        with open(request_file, 'r') as f:
            data = json.load(f)
        
        request_id = data.get('request_id', str(uuid.uuid4()))
        action = data.get('action', 'chat')
        payload = data.get('payload', {})
        message = payload.get('message', '')
        
        log(f"Memproses request: {request_id} | Aksi: {action}")

        # Proses berdasarkan aksi
        if action == 'chat':
            response_text = get_hermes_response(message)
        else:
            response_text = f"Aksi '{action}' diterima, namun bridge saat ini hanya mendukung 'chat'."

        # Buat objek respons
        response_data = {
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success",
            "payload": {
                "message": response_text
            }
        }

        # Tulis file respons
        response_filename = f"response_{request_id}.json"
        response_path = OUTGOING_DIR / response_filename
        with open(response_path, 'w') as f:
            json.dump(response_data, f, indent=2)
        
        log(f"Respons terkirim: {response_filename}")

        # Hapus file request yang sudah diproses agar tidak menumpuk
        os.remove(request_file)

    except json.JSONDecodeError:
        log(f"Error: File {request_file.name} bukan JSON valid.")
        os.remove(request_file) # Hapus file rusak
    except Exception as e:
        log(f"Error memproses {request_file.name}: {e}")

def main():
    log("==========================================")
    log("⚕️ Hermes Bridge Service Started (Fixed)")
    log(f"📂 Monitoring: {INCOMING_DIR}")
    log("==========================================")

    while True:
        try:
            # Cari file json di folder incoming
            files = list(INCOMING_DIR.glob("*.json"))
            
            for req_file in files:
                process_request(req_file)
                
        except KeyboardInterrupt:
            log("Service dihentikan oleh user.")
            break
        except Exception as e:
            log(f"Error utama: {e}")
        
        time.sleep(1) # Jeda 1 detik untuk menghemat CPU

if __name__ == "__main__":
    main()
