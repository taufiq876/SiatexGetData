```markdown
<p align="center">
  <img src="https://img.shields.io/badge/Status-Aktif-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Lisensi-MIT-orange" alt="Lisensi">
</p>

<h1 align="center">SIAtex Data Toolkit</h1>

<p align="center">
  <strong>Tools otomatis untuk mengambil data siswa dari SIAtex SMK Texmaco Semarang.</strong><br>
  Dirancang untuk keperluan pendidikan, riset, dan pengelolaan data internal secara efisien & bertanggung jawab.
</p>

---

## 🚀 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Auto Download Data Siswa** | Script Python yang login otomatis & menyimpan data JSON per siswa. |
| **Unduh Daftar NIS** | Bookmarklet satu baris untuk mengambil daftar NIS & nama dari halaman Pengajuan PKL. |
| **Logging & Progress** | Log berwarna, progress bar, dan fitur *resume* agar proses tidak terputus. |

---

## 📁 Struktur Repository

```text
SIAtex-Data-Toolkit/
├── download_siatex.py        # Script Python auto-download
├── list_nis_bookmarklet.js   # Bookmarklet unduh daftar NIS
├── data/                     # Folder hasil download
│   ├── 241657.json
│   ├── 247945.json
│   └── ...
└── README.md                 # Dokumentasi
```

---

⚙️ Cara Pakai Script Python (Auto Download)

1. Install Dependensi

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

```text
https://raw.githubusercontent.com/taufiq876/DataNis/main/Data/List_Nis_Siatex.json
```

4. Hasil Otomatis

· Semua file JSON tersimpan di: ~/storage/downloads/DaftarNis/
· Format file: {NIS}.json (terpisah per siswa)
· Otomatis melewati siswa yang sudah terdownload

---

📌 Tutorial Bookmarklet Unduh List NIS

⚠️ PENTING: Bookmarklet hanya berfungsi setelah login dan berada di halaman Pengajuan PKL.

Langkah-Langkah:

1. Login SIAtex

Buka https://siatex-v2.smktexmaco-smg.sch.id dan login dengan akun siswa.

2. Masuk ke Menu Pengajuan PKL

Klik menu HUBINMAS → Pengajuan PKL (Siswa).

3. Klik Tombol Tambah

Tekan tombol Tambah / Create untuk membuka form input.

4. Jalankan Bookmarklet

Paste script berikut di address bar, lalu tekan Enter:

```javascript
javascript:(function(){
  var ja = document.querySelector('#jumlah_anggota');
  if (ja) {
    ja.value = '1';
    ja.dispatchEvent(new Event('input', { bubbles: true }));
  }
  var t = setInterval(function(){
    var s = document.querySelector('select[name="nisis_sis[]"]');
    if (!s) return;
    clearInterval(t);
    var o = s.querySelectorAll('option'), sis = [], seen = {};
    o.forEach(function(x){
      var v = x.value.trim();
      if (!v || v === '' || seen[v]) return;
      seen[v] = true;
      var n = x.textContent.trim().replace(new RegExp('^' + v.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*-\\s*'), '');
      sis.push({ nis: v, nama: n });
    });
    var d = { total: sis.length, siswa: sis };
    var b = new Blob([JSON.stringify(d, null, 2)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(b);
    a.download = 'List_Nis_Siatex.json';
    a.click();
  }, 1000);
})();
```

5. File Terunduh Otomatis

File List_Nis_Siatex.json langsung terdownload berisi daftar NIS & nama siswa.

---

🛡️ Catatan Penting

· Gunakan tools ini hanya untuk keperluan yang sah (pendidikan, riset, pengelolaan data internal).
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

<p align="center">
  Dibuat dengan ❤️ untuk kemajuan pendidikan Indonesia 🇮🇩
</p>
```
