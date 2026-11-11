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

---

## 👥 Panduan untuk Teman: Cara Kustomisasi Matkul & Jadwal Sendiri

Jika temanmu ingin menggunakan repositori ini untuk jadwal matkul dan akunnya sendiri, ikuti 5 langkah mudah berikut:

### Langkah 1: Buat Repositori Sendiri (Wajib PRIVATE)
1. **PENTING**: Jangan jadikan repositori publik karena mengandung jadwal perkuliahan pribadi.
2. Buat repositori baru di GitHub dengan status **Private**.
3. Clone / copy file dari repositori ini ke repositori baru milik temanmu.

---

### Langkah 2: Cari Link & ID Matkul dari SPADA UPNYK
Buka [SPADA UPNYK](https://spada.upnyk.ac.id), lalu untuk setiap matkul:
1. **Link Halaman Matkul**:
   - Buka matkul yang diambil, lihat URL di address bar browser:
     `https://spada.upnyk.ac.id/course/view.php?id=56302`
   - Angka `56302` adalah **`course_id`**.
2. **Link Halaman Presensi (Attendance)**:
   - Klik menu **Presensi / Kehadiran / Attendance** di dalam matkul tersebut.
   - Lihat URL di address bar:
     `https://spada.upnyk.ac.id/mod/attendance/view.php?id=813446`
   - Angka `813446` adalah **`attendance_id`**, dan seluruh URL tersebut adalah **`attendance_url`**.

---

### Langkah 3: Ubah Konfigurasi Matkul (`config/courses.json`)
Buka file `config/courses.json` dan sesuaikan daftar matkulnya. 

#### Contoh Struktur 1 Matkul:
```json
{
  "id": "nama-singkat-matkul",
  "name": "Nama Lengkap Matkul",
  "day": "Monday",
  "day_id": "Senin",
  "start_time": "10:00",
  "end_time": "12:30",
  "course_id": "56302",
  "attendance_id": "813446",
  "attendance_url": "https://spada.upnyk.ac.id/mod/attendance/view.php?id=813446",
  "enabled": true
}
```

#### Penjelasan Kolom:
- **`id`**: Identifier unik, gunakan huruf kecil tanpa spasi (misal: `basis-data`, `pbo`, `jarkom`).
- **`name`**: Nama mata kuliah (ditampilkan di notifikasi Telegram).
- **`day`**: Hari dalam bahasa Inggris: `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, atau `Sunday`.
- **`day_id`**: Hari dalam bahasa Indonesia: `Senin`, `Selasa`, `Rabu`, `Kamis`, `Jumat`, `Sabtu`, atau `Minggu`.
- **`start_time`**: Jam mulai kelas dalam format 24 jam WIB (`HH:MM`, contoh: `"07:30"`).
- **`end_time`**: Jam selesai kelas dalam format 24 jam WIB (`HH:MM`, contoh: `"10:00"`).
- **`course_id`**: ID matkul dari URL SPADA.
- **`attendance_id`**: ID attendance dari URL SPADA.
- **`attendance_url`**: URL lengkap halaman attendance.
- **`enabled`**: `true` untuk aktifkan auto-presensi, atau `false` untuk mematikan sementara.

---

### Langkah 4: Atur Jadwal Otomatis (Cron) di `.github/workflows/presence.yml`

GitHub Actions berjalan di server cloud dengan patokan zona waktu **UTC (Universal Time Coordinated)**. Sedangkan Indonesia bagian barat menggunakan **WIB (UTC + 7)**.

#### 🧮 Rumus Konversi WIB ke UTC:
$$\text{Jam UTC} = \text{Jam WIB} - 7$$

#### ⏰ Tabel Konversi Cepat (WIB ➔ UTC):
| Jam Kuliah di Kampus (WIB) | Jam di Server GitHub (UTC) |
| :---: | :---: |
| 07:00 WIB | 00:00 UTC |
| 08:00 WIB | 01:00 UTC |
| 09:00 WIB | 02:00 UTC |
| 10:00 WIB | 03:00 UTC |
| 11:00 WIB | 04:00 UTC |
| 12:00 WIB | 05:00 UTC |
| 13:00 WIB | 06:00 UTC |
| 14:00 WIB | 07:00 UTC |
| 15:00 WIB | 08:00 UTC |
| 16:00 WIB | 09:00 UTC |
| 17:00 WIB | 10:00 UTC |

#### 📅 Angka Hari dalam Cron GitHub:
| Hari | Nilai Cron |
| :---: | :---: |
| Minggu | `0` |
| Senin | `1` |
| Selasa | `2` |
| Rabu | `3` |
| Kamis | `4` |
| Jumat | `5` |
| Sabtu | `6` |

#### ⚙️ Cara Menulis Jadwal Cron:
Buka `.github/workflows/presence.yml` pada bagian `schedule:`.
Disarankan menggunakan format **pengecekan interval tiap 10 menit (`*/10`)** selama jam kuliah berlangsung, agar jika dosen baru membuka presensi di tengah perkuliahan, bot tetap bisa klik hadir.

**Format syntax cron:**
```text
- cron: '*/10 <rentang_jam_utc> * * <hari>'
```

**Contoh Kasus:**
1. **Matkul A**: Hari **Senin** jam **10:00 - 12:30 WIB**
   - Hari: Senin = `1`
   - Jam 10:00 WIB = 03:00 UTC | Jam 12:30 WIB = 05:30 UTC
   - Rentang jam UTC: `3-5`
   - Cron-nya: `- cron: '*/10 3-5 * * 1'`

2. **Matkul B**: Hari **Rabu** jam **07:30 - 10:00 WIB**
   - Hari: Rabu = `3`
   - Jam 07:30 WIB = 00:30 UTC | Jam 10:00 WIB = 03:00 UTC
   - Rentang jam UTC: `0-3`
   - Cron-nya: `- cron: '*/10 0-3 * * 3'`

3. **Matkul C**: Hari **Jumat** jam **13:00 - 15:30 WIB**
   - Hari: Jumat = `5`
   - Jam 13:00 WIB = 06:00 UTC | Jam 15:30 WIB = 08:30 UTC
   - Rentang jam UTC: `6-8`
   - Cron-nya: `- cron: '*/10 6-8 * * 5'`

#### 💡 Jangan Lupa Update Dropdown Manual:
Di file `.github/workflows/presence.yml`, pada bagian `workflow_dispatch` -> `options`, ganti daftar pilihan matkul sesuai dengan `id` matkul yang baru dibuat, contoh:
```yaml
        options:
          - auto
          - all
          - basis-data
          - jarkom
          - pbo
```

---

### Langkah 5: Masukkan Kredensial Pribadi ke GitHub Secrets
Temanmu harus memasukkan akun SPADA dan bot Telegram miliknya sendiri ke repositori GitHub miliknya:
1. Masuk ke repo GitHub miliknya > **Settings** > **Secrets and variables** > **Actions**.
2. Klik **New repository secret** dan buat 4 secrets:
   - `SPADA_USERNAME`: NIM temanmu.
   - `SPADA_PASSWORD`: Password portal SPADA temanmu.
   - `TELEGRAM_BOT_TOKEN`: Token API bot Telegram miliknya (dibuat via `@BotFather`).
   - `TELEGRAM_CHAT_ID`: ID akun Telegram miliknya (didapat via `@userinfobot`).

Selesai! Sekarang repositori temanmu akan berjalan otomatis sesuai jadwal matkulnya sendiri 24/7 di cloud! 🚀

