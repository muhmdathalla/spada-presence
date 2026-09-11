# 🎓 SPADA UPNYK Auto-Presence (Semester 5)

Sistem presensi otomatis untuk portal e-Learning SPADA UPN "Veteran" Yogyakarta (`spada.upnyk.ac.id`) menggunakan Python + Playwright, dilengkapi notifikasi bukti hadir ke Telegram, serta penjadwalan cloud 24/7 dengan GitHub Actions.

---

## 📋 Daftar Matkul Terdaftar (Semester 5)

| No | Matkul | Hari | Jam (WIB) | ID Matkul | ID Presensi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Sistem Operasi** | Senin | 10.00 - 12.30 | `56302` | `813446` |
| 2 | **Praktikum Data Science** | Senin | 13.00 - 13.15 | `55072` | `818308` |
| 3 | **Administrasi Server** | Senin | 14.50 - 15.30 | `51155` | `807431` |
| 4 | **Internet of Things (IoT)** | Selasa | 07.00 - 10.00 | `52503` | `807829` |
| 5 | **Manajemen Proyek Perangkat Lunak** | Selasa | 10.00 - 12.00 | `53174` | `805438` |
| 6 | **Praktikum IoT** | Selasa | 13.00 - 13.15 | `55425` | `814209` |
| 7 | **Kriptografi** | Kamis | 07.25 - 07.45 | `52919` | `805752` |
| 8 | **Data Science** | Kamis | 12.30 - 12.45 | `51777` | `809101` |
| 9 | **Pengolahan Citra** | Jumat | 13.00 - 15.30 | `54566` | `808663` |
| 10 | **Penginderaan Jarak Jauh** | Jumat | 15.30 - 18.00 | `54561` | `811820` |
| 11 | **Kapita Selekta** | Sabtu | 07.00 - 09.00 | `52579` | `808956` |

---

## 🚀 Panduan Setup GitHub Actions (Otomatis Cloud 24/7)

Agar script berjalan otomatis di server GitHub tanpa perlu membuka laptop:

### Langkah 1: Buat Repositori GitHub Baru (PRIVATE)
1. Buka [GitHub](https://github.com) dan buat repositori baru (contoh: `spada-presence`).
2. **PENTING**: Pilih opsi **Private** agar username dan data kamu aman.
3. Push folder ini ke repositori tersebut:
   ```bash
   git init
   git add .
   git commit -m "Initial commit auto presence"
   git branch -M main
   git remote add origin https://github.com/USERNAME_KAMU/spada-presence.git
   git push -u origin main
   ```

### Langkah 2: Buat Bot Telegram (Gratis)
1. Buka Telegram, cari akun `@BotFather`
2. Ketik `/newbot`, ikuti petunjuk dan beri nama botmu (misal: `SpadaPresensiBot`).
3. Kamu akan mendapatkan **API Token** (contoh: `123456789:ABCdefGhIJKlmNo...`).
4. Cari akun `@userinfobot` atau `@raw_data_bot` di Telegram untuk mengetahui **Chat ID** akun Telegram kamu (angka ID kamu).
5. Klik **Start** pada bot yang baru kamu buat agar bot bisa mengirim pesan ke kamu.

### Langkah 3: Masukkan Secrets di GitHub
1. Di repositori GitHub kamu, buka menu **Settings** > **Secrets and variables** > **Actions**.
2. Klik tombol **New repository secret** dan tambahkan secret berikut:

| Nama Secret | Nilai / Value |
| :--- | :--- |
| `SPADA_USERNAME` | `123240212` |
| `SPADA_PASSWORD` | `Athallaupn2024_` |
| `TELEGRAM_BOT_TOKEN` | Token dari BotFather |
| `TELEGRAM_CHAT_ID` | Chat ID Telegram kamu |

### Langkah 4: Selesai & Aktif!
- GitHub Actions akan otomatis bangun dan melakukan presensi setiap jam matkul dimulai.
- Kamu juga bisa memicu presensi manual kapan saja:
  1. Masuk ke tab **Actions** di repo GitHub.
  2. Pilih workflow **SPADA UPNYK Auto Presence**.
  3. Klik **Run workflow** -> pilih matkul -> klik **Run**.

---

## 💻 Panduan Menjalankan di Lokal (MacBook / Windows)

### 1. Install Dependensi
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Jalankan Perintah
- **Lihat daftar matkul:**
  ```bash
  python main.py --list
  ```
- **Presensi matkul tertentu (contoh: Kapita Selekta):**
  ```bash
  python main.py --course kapita-selekta
  ```
- **Presensi dengan token/password dosen:**
  ```bash
  python main.py --course kriptografi --token 123456
  ```
- **Auto presensi sesuai jadwal saat ini:**
  ```bash
  python main.py --auto
  ```
- **Lihat browser saat berjalan (bukan headless):**
  ```bash
  python main.py --course iot --headless false
  ```
