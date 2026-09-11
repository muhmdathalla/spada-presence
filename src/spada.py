import os
import time
import logging
from datetime import datetime, timezone, timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:
    try:
        import pytz
        ZoneInfo = lambda tz_name: pytz.timezone(tz_name)
    except ImportError:
        ZoneInfo = None

logger = logging.getLogger("SpadaPresence")

def get_now_wib():
    if ZoneInfo:
        try:
            return datetime.now(ZoneInfo(os.getenv("TIMEZONE", "Asia/Jakarta")))
        except Exception:
            pass
    return datetime.now(timezone(timedelta(hours=7)))

class SpadaAttendance:
    def __init__(self, username=None, password=None, headless=True):
        self.username = username or os.getenv("SPADA_USERNAME")
        self.password = password or os.getenv("SPADA_PASSWORD")
        self.headless = headless if isinstance(headless, bool) else (os.getenv("HEADLESS", "true").lower() == "true")
        self.base_url = "https://spada.upnyk.ac.id"
        self.login_url = f"{self.base_url}/login/index.php"

        if not self.username or not self.password:
            raise ValueError("SPADA_USERNAME and SPADA_PASSWORD must be configured in .env or environment!")

    def _ensure_dir(self, path):
        os.makedirs(path, exist_ok=True)

    def run_attendance(self, course: dict, password_token: str = None) -> dict:
        """
        Executes presence for a specific course.
        Returns dict with keys: status, message, screenshot_path, course_name, timestamp
        """
        from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

        course_name = course.get("name", "Unknown Course")
        attendance_url = course.get("attendance_url")
        course_id = course.get("id", "course")
        
        now_wib = get_now_wib()
        timestamp_str = now_wib.strftime("%Y-%m-%d_%H-%M-%S")
        human_time = now_wib.strftime("%d %B %Y, %H:%M:%S WIB")

        self._ensure_dir("screenshots")
        screenshot_path = f"screenshots/{course_id}_{timestamp_str}.png"

        result = {
            "status": "FAILED",
            "message": "",
            "screenshot_path": None,
            "course_name": course_name,
            "timestamp": human_time
        }

        logger.info(f"Starting attendance process for: {course_name}")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                # 1. Login Step
                logger.info(f"Navigating to login page: {self.login_url}")
                page.goto(self.login_url, wait_until="domcontentloaded", timeout=45000)

                # Check if login form is present
                if page.locator("#username").is_visible(timeout=5000):
                    logger.info("Filling credentials...")
                    page.fill("#username", self.username)
                    page.fill("#password", self.password)
                    page.click("#loginbtn")
                    page.wait_for_load_state("domcontentloaded", timeout=30000)

                    # Check for login error
                    if page.locator(".alert-danger, .loginerrors").is_visible(timeout=3000):
                        error_text = page.locator(".alert-danger, .loginerrors").first.inner_text()
                        result["status"] = "LOGIN_FAILED"
                        result["message"] = f"Gagal login ke SPADA: {error_text.strip()}"
                        page.screenshot(path=screenshot_path, full_page=True)
                        result["screenshot_path"] = screenshot_path
                        browser.close()
                        return result

                logger.info("Login verified.")

                # 2. Navigate to Attendance Page
                logger.info(f"Opening attendance page: {attendance_url}")
                page.goto(attendance_url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(2000)

                # 3. Detect Submit Attendance button
                submit_selectors = [
                    "a:has-text('Submit attendance')",
                    "a:has-text('Ajukan kehadiran')",
                    "a:has-text('Submit')",
                    "a[href*='attendance.php?sessid=']",
                    "a[href*='attendance_view_student.php']"
                ]

                submit_btn = None
                for selector in submit_selectors:
                    loc = page.locator(selector).first
                    if loc.is_visible(timeout=2000):
                        submit_btn = loc
                        logger.info(f"Found attendance submit button: {selector}")
                        break

                if submit_btn:
                    logger.info("Navigating to submission form...")
                    submit_btn.click()
                    page.wait_for_load_state("domcontentloaded", timeout=30000)
                    page.wait_for_timeout(2000)

                    # 4. Fill Attendance Form (Select 'Hadir' / 'Present')
                    radio_found = False
                    present_labels = [
                        "label:has-text('Present')",
                        "label:has-text('Hadir')",
                        "label:has-text('H')",
                        "span:has-text('Present')",
                        "span:has-text('Hadir')"
                    ]
                    for plabel in present_labels:
                        loc = page.locator(plabel).first
                        if loc.is_visible(timeout=1500):
                            loc.click()
                            radio_found = True
                            logger.info(f"Selected 'Hadir / Present' via: {plabel}")
                            break

                    if not radio_found:
                        radio_inputs = page.locator("input[type='radio']")
                        if radio_inputs.count() > 0:
                            radio_inputs.first.click()
                            radio_found = True
                            logger.info("Selected first available radio option.")

                    # Password / Token check
                    password_inputs = page.locator("input[name='studentpassword'], #id_studentpassword, input[name='qrpass']")
                    if password_inputs.is_visible(timeout=1000):
                        if password_token:
                            logger.info(f"Entering attendance password: {password_token}")
                            password_inputs.fill(password_token)
                        else:
                            logger.warning("Attendance requires a password/token but none was provided!")
                            result["status"] = "PASSWORD_REQUIRED"
                            result["message"] = "Presensi memerlukan Password / Token dari Dosen!"
                            page.screenshot(path=screenshot_path, full_page=True)
                            result["screenshot_path"] = screenshot_path
                            browser.close()
                            return result

                    # 5. Save Changes
                    save_selectors = [
                        "#id_submitbutton",
                        "input[name='submitbutton']",
                        "button[type='submit']",
                        "input[type='submit'][value*='Save']",
                        "input[type='submit'][value*='Simpan']"
                    ]
                    for save_sel in save_selectors:
                        save_btn = page.locator(save_sel).first
                        if save_btn.is_visible(timeout=2000):
                            save_btn.click()
                            logger.info(f"Submitted form via {save_sel}")
                            break

                    page.wait_for_load_state("domcontentloaded", timeout=30000)
                    page.wait_for_timeout(2000)

                    page.screenshot(path=screenshot_path, full_page=True)
                    result["screenshot_path"] = screenshot_path
                    result["status"] = "SUCCESS"
                    result["message"] = f"✅ Berhasil presensi (Hadir) untuk matkul {course_name}!"
                    logger.info(result["message"])

                else:
                    page_text = page.inner_text("body")
                    page.screenshot(path=screenshot_path, full_page=True)
                    result["screenshot_path"] = screenshot_path

                    if "Present" in page_text or "Hadir" in page_text:
                        result["status"] = "ALREADY_SUBMITTED"
                        result["message"] = f"ℹ️ Sesi presensi matkul {course_name} sudah tercatat Hadir sebelumnya."
                        logger.info(result["message"])
                    else:
                        result["status"] = "NOT_OPEN"
                        result["message"] = f"⏳ Sesi presensi untuk matkul {course_name} saat ini belum dibuka."
                        logger.info(result["message"])

            except PlaywrightTimeoutError as te:
                logger.error(f"Timeout during attendance: {te}")
                try:
                    page.screenshot(path=screenshot_path, full_page=True)
                    result["screenshot_path"] = screenshot_path
                except Exception:
                    pass
                result["status"] = "TIMEOUT"
                result["message"] = f"⚠️ Timeout saat mengakses SPADA untuk matkul {course_name}."

            except Exception as e:
                logger.error(f"Error during attendance: {e}", exc_info=True)
                try:
                    page.screenshot(path=screenshot_path, full_page=True)
                    result["screenshot_path"] = screenshot_path
                except Exception:
                    pass
                result["status"] = "ERROR"
                result["message"] = f"❌ Terjadi kesalahan saat presensi {course_name}: {str(e)}"

            finally:
                browser.close()

        return result
