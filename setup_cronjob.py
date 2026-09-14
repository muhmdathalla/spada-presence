"""
Setup Helper for SPADA Remote Auto-Presence via cron-job.org or GitHub API.
"""
import sys
import json
import urllib.request
import urllib.error

REPO = "muhmdathalla/spada-presence"

def test_github_trigger(github_pat: str):
    url = f"https://api.github.com/repos/{REPO}/dispatches"
    headers = {
        "Authorization": f"Bearer {github_pat}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "SpadaAutoPresence"
    }
    payload = json.dumps({"event_type": "auto-presence"}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in [200, 204]:
                print("✅ Berhasil memicu GitHub Actions dari jarak jauh (Remote Trigger Sukses)!")
                return True
    except urllib.error.HTTPError as e:
        print(f"❌ Gagal memicu GitHub: HTTP {e.code} - {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_cronjob_org(cronjob_api_key: str, github_pat: str):
    url = "https://api.cron-job.org/jobs"
    headers = {
        "Authorization": f"Bearer {cronjob_api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "job": {
            "url": f"https://api.github.com/repos/{REPO}/dispatches",
            "title": "SPADA UPNYK Auto Presence",
            "enabled": True,
            "saveResponses": True,
            "schedule": {
                "timezone": "Asia/Jakarta",
                "hours": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                "mdays": [-1],
                "minutes": [2, 15, 30, 45],
                "months": [-1],
                "wdays": [1, 2, 4, 5, 6]
            },
            "requestMethod": 1,
            "requestBody": json.dumps({"event_type": "auto-presence"}),
            "extendedData": {
                "headers": {
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {github_pat}",
                    "User-Agent": "CronJob-SpadaAutoPresence"
                }
            }
        }
    }

    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            job_id = data.get("jobId")
            print(f"🎉 Sukses mendaftarkan remote schedule ke cron-job.org! Job ID: {job_id}")
            print("Sistem sekarang sudah 100% otomatis tanpa perlu menyentuh laptop atau tombol apa pun!")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ Gagal mendaftarkan cron job: HTTP {e.code} - {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan:")
        print("  1. Tes Trigger Remote:")
        print("     python setup_cronjob.py test <GITHUB_PAT>")
        print("  2. Otomatis Pasang Jadwal ke cron-job.org:")
        print("     python setup_cronjob.py setup <CRONJOB_API_KEY> <GITHUB_PAT>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "test":
        pat = sys.argv[2]
        test_github_trigger(pat)
    elif cmd == "setup":
        cron_key = sys.argv[2]
        pat = sys.argv[3]
        create_cronjob_org(cron_key, pat)
