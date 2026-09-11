import os
import sys
import json
import argparse
import logging

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from src.scheduler import load_courses, get_current_courses

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("Main")

def process_course(spada, notifier, course: dict, token: str = None):
    course_name = course.get("name")
    logger.info(f"=== Memproses Presensi: {course_name} ===")
    
    res = spada.run_attendance(course, password_token=token)
    
    status_icon = "✅" if res["status"] == "SUCCESS" else ("ℹ️" if res["status"] == "ALREADY_SUBMITTED" else "⚠️")
    
    caption = (
        f"{status_icon} <b>Laporan Presensi SPADA UPNYK</b>\n\n"
        f"📚 <b>Matkul:</b> {res['course_name']}\n"
        f"📅 <b>Waktu:</b> {res['timestamp']}\n"
        f"📌 <b>Status:</b> {res['status']}\n"
        f"💬 <b>Keterangan:</b> {res['message']}\n"
    )

    if res.get("screenshot_path") and os.path.exists(res["screenshot_path"]):
        notifier.send_photo(res["screenshot_path"], caption=caption)
    else:
        notifier.send_message(caption)

    return res

def main():
    parser = argparse.ArgumentParser(description="SPADA UPNYK Automated Attendance Bot")
    parser.add_argument("--course", type=str, help="ID, nama, atau Course ID matkul yang ingin dipresensi")
    parser.add_argument("--all", action="store_true", help="Jalankan presensi untuk semua matkul yang terdaftar")
    parser.add_argument("--auto", action="store_true", help="Otomatis jalankan presensi untuk matkul yang jadwalnya aktif saat ini")
    parser.add_argument("--token", type=str, help="Password / Token presensi yang diberikan dosen (opsional)")
    parser.add_argument("--headless", type=str, default="true", help="Mode headless browser (true/false)")
    parser.add_argument("--list", action="store_true", help="Tampilkan daftar semua matkul yang terdaftar")

    args = parser.parse_args()

    courses = load_courses()
    
    if args.list:
        print("\n=== DAFTAR 11 MATKUL TERDAFTAR (SEMESTER 5) ===")
        for idx, c in enumerate(courses, 1):
            print(f"{idx:2d}. [{c['id']}] {c['name']}")
            print(f"    📅 Jadwal : {c['day_id']}, {c['start_time']} - {c['end_time']} WIB")
            print(f"    🔗 Presensi: {c['attendance_url']}")
        print("================================================\n")
        return

    from src.spada import SpadaAttendance
    from src.notifier import TelegramNotifier

    is_headless = args.headless.lower() == "true"
    spada = SpadaAttendance(headless=is_headless)
    notifier = TelegramNotifier()

    if args.course:
        target_course = None
        for c in courses:
            if (args.course.lower() in c.get("id", "").lower() or 
                args.course.lower() in c.get("name", "").lower() or 
                args.course == c.get("course_id") or 
                args.course == c.get("attendance_id")):
                target_course = c
                break
        
        if not target_course:
            logger.error(f"Matkul dengan kueri '{args.course}' tidak ditemukan di config/courses.json!")
            sys.exit(1)

        process_course(spada, notifier, target_course, token=args.token)

    elif args.all:
        logger.info("Menjalankan presensi untuk SELURUH matkul yang aktif di konfigurasi...")
        for c in courses:
            if c.get("enabled", True):
                process_course(spada, notifier, c, token=args.token)

    elif args.auto:
        current_courses = get_current_courses(courses, tolerance_minutes=15)
        if not current_courses:
            logger.info("Tidak ada jadwal matkul yang aktif pada jam dan hari ini.")
            return
        
        logger.info(f"Ditemukan {len(current_courses)} matkul yang aktif saat ini. Memulai proses presensi...")
        for c in current_courses:
            process_course(spada, notifier, c, token=args.token)

    else:
        current_courses = get_current_courses(courses, tolerance_minutes=15)
        if not current_courses:
            logger.info("Tidak ada jadwal matkul yang aktif pada jam dan hari ini. Gunakan --list untuk melihat jadwal atau --course <id> untuk tes.")
            return
        for c in current_courses:
            process_course(spada, notifier, c, token=args.token)

if __name__ == "__main__":
    main()
