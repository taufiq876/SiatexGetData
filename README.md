Oke, Raden. Ini README.md lengkap dalam satu blok, siap salin langsung. Tampilan rapi, modern, dan mencakup semua fitur + tutorial.

---

```markdown
# 🎓 SIAtex Data Toolkit

**Kumpulan tools otomatis untuk mengambil data siswa dari SIAtex SMK Texmaco Semarang.**  
Didesain untuk keperluan pendidikan, riset, dan pengelolaan data internal secara efisien dan bertanggung jawab.

---

## ✨ Fitur Utama

- **Auto Download Data Siswa**  
  Script Python yang login otomatis dan menyimpan data JSON setiap siswa secara terpisah.

- **Unduh Daftar NIS**  
  Bookmarklet satu baris untuk mengambil daftar NIS & nama dari halaman Pengajuan PKL.

- **Logging & Progress**  
  Log berwarna, progress bar, dan fitur *resume* agar proses tidak terputus.

---

## 📂 Struktur Repository

```

├── download_siatex.py        # Script Python auto-download data siswa
├── list_nis_bookmarklet.js   # Bookmarklet unduh daftar NIS
├── data/                     # Folder hasil download (JSON per siswa)
│   ├── 241657.json
│   ├── 247945.json
│   └── ...
└── README.md                 # Dokumentasi ini

```

---

## ⚙️ Cara Pakai Script Python (Auto Download)

### 1. Install Dependensi

```bash
pkg update && pkg upgrade
pkg install python python-pip
pip install requests beautifulsoup4
```

2. Jalankan Script

```bash
python download_siatex.py
```

3. Input Link GitHub

Saat diminta, masukkan link raw dari file JSON daftar NIS.
Contoh:

```
https://raw.githubusercontent.com/taufiq876/DataNis/main/Data/List_Nis_Siatex.json
```

4. Hasil Otomatis

· Semua file JSON tersimpan di: ~/storage/downloads/DaftarNis/
· Format file: {NIS}.json (terpisah per siswa)
· Otomatis melewati siswa yang sudah terdownload

---

📌 Tutorial Bookmarklet Unduh List NIS

⚠️ PENTING: Bookmarklet hanya berfungsi setelah login dan berada di halaman Pengajuan PKL.

Langkah-langkah:

1. Login SIAtex

Buka https://siatex-v2.smktexmaco-smg.sch.id dan login dengan akun siswa.

2. Masuk ke Menu Pengajuan PKL

Klik menu HUBINMAS → Pengajuan PKL (Siswa).

3. Klik Tombol Tambah

Tekan tombol Tambah / Create untuk membuka form input.

4. Jalankan Bookmarklet

Paste script berikut di address bar, lalu tekan Enter:

```
javascript:(function(){var ja=document.querySelector('#jumlah_anggota');if(ja){ja.value='1';ja.dispatchEvent(new Event('input',{bubbles:true}));}var t=setInterval(function(){var s=document.querySelector('select[name="nisis_sis[]"]');if(!s)return;clearInterval(t);var o=s.querySelectorAll('option'),sis=[],seen={};o.forEach(function(x){var v=x.value.trim();if(!v||v===''||seen[v])return;seen[v]=true;var n=x.textContent.trim().replace(new RegExp('^'+v.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\s*-\\s*'),'');sis.push({nis:v,nama:n});});var d={total:sis.length,siswa:sis};var b=new Blob([JSON.stringify(d,null,2)],{type:'application/json'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='List_Nis_Siatex.json';a.click();},1000);})();
```

5. File Terunduh Otomatis

File List_Nis_Siatex.json langsung terdownload berisi daftar NIS & nama siswa.

---

🛡️ Catatan Penting

· Gunakan tools ini hanya untuk keperluan yang sah (pendidikan, riset, atau pengelolaan data internal).
· Jangan menyebarkan data pribadi siswa tanpa izin.
· Jangan membebani server dengan request berlebihan.
· Semua risiko penggunaan sepenuhnya tanggung jawab pengguna.

---

🤝 Kontribusi

Pull request & saran sangat diterima.
Jika menemukan bug, silakan buka issue di repo ini.

---

📜 Lisensi

MIT License – bebas digunakan & dimodifikasi dengan tetap mencantumkan atribusi.

---

Dibuat dengan ❤️ untuk kemajuan pendidikan Indonesia 🇮🇩

```

---

Tinggal **copy semua** dari atas sampai bawah, paste ke file `README.md` di repo GitHub, commit, dan tampilan repo kamu langsung keren. Kalau mau ditambah badge atau screenshot, bilang saja, Raden.
