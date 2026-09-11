import json
import os
import time
import logging
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:
    try:
        import pytz
        ZoneInfo = lambda tz_name: pytz.timezone(tz_name)
    except ImportError:
        ZoneInfo = None

logger = logging.getLogger("SpadaScheduler")

def get_now_wib():
    if ZoneInfo:
        try:
            return datetime.now(ZoneInfo("Asia/Jakarta"))
        except Exception:
            pass
    # Fallback UTC+7
    return datetime.now(timezone(timedelta(hours=7)))

def load_courses(config_path="config/courses.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_current_courses(courses: list, tolerance_minutes=15) -> list:
    """
    Finds courses that are active right now or starting within tolerance_minutes.
    """
    now = get_now_wib()
    current_day = now.strftime("%A")  # e.g. Monday, Tuesday
    current_time_str = now.strftime("%H:%M")
    current_time = datetime.strptime(current_time_str, "%H:%M").time()

    active_courses = []
    for course in courses:
        if not course.get("enabled", True):
            continue

        course_day = course.get("day")
        if course_day.lower() != current_day.lower():
            continue

        start_str = course.get("start_time")
        end_str = course.get("end_time")
        
        try:
            start_t = datetime.strptime(start_str, "%H:%M")
            end_t = datetime.strptime(end_str, "%H:%M")
            
            # Start tolerance window: tolerance_minutes before start_time up to end_time
            window_start = (start_t - timedelta(minutes=tolerance_minutes)).time()
            window_end = end_t.time()

            if window_start <= current_time <= window_end:
                active_courses.append(course)
        except Exception as e:
            logger.error(f"Error parsing time for course {course.get('name')}: {e}")

    return active_courses
