import requests
import json
import time
import datetime


API_LOGIN = "https://airdrop-api-dot-life-airdrop.du.r.appspot.com/api/v1/auth-header/google"
API_CHECKIN = "https://airdrop-api-dot-life-airdrop.du.r.appspot.com/api/v1/attendance/check-in"
API_TASK = "https://airdrop-api-dot-life-airdrop.du.r.appspot.com/api/v1/mission/daily/submit"
DATA_FILE = "data.txt"


def read_tokens():
    tokens = []
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    tokens.append({"idToken": parts[0], "userEmail": parts[1]})
                elif len(parts) == 1:
                    tokens.append({"idToken": parts[0], "userEmail": None})
        return tokens
    except FileNotFoundError:
        print(f"❌ File {DATA_FILE} tidak ditemukan!")
        return []

def login_with_idtoken(id_token, user_email=None):
    payload = {"idToken": id_token, "userEmail": user_email or ""}
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://airdrop.lifenetworks.io",
        "referer": "https://airdrop.lifenetworks.io/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        res = requests.post(API_LOGIN, headers=headers, data=json.dumps(payload))
        if res.status_code == 201:
            data = res.json().get("data", {})
            return {
                "email": data.get("userEmail"),
                "userId": data.get("userId"),
                "credit": data.get("userCredit"),
                "point": data.get("userPoint"),
                "accessToken": data.get("accessToken")
            }
        else:
            return {"error": f"HTTP {res.status_code}: {res.text}"}
    except Exception as e:
        return {"error": str(e)}

def daily_checkin(access_token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
        "origin": "https://airdrop.lifenetworks.io",
        "referer": "https://airdrop.lifenetworks.io/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        res = requests.post(API_CHECKIN, headers=headers)
        if res.status_code == 201:
            data = res.json().get("data", {})
            return {
                "status": "✅ Sukses",
                "earned": data.get("earnedPoints", "0"),
                "total": data.get("newTotalPoints", "?"),
                "day": data.get("attendanceDay", "?"),
            }
        elif res.status_code == 409:
            return {
                "status": "⏳ Sudah check-in hari ini",
                "earned": "0",
                "total": "-",
                "day": "-"
            }
        else:
            return {"status": f"❌ Gagal ({res.status_code})", "earned": "-", "total": "-", "day": "-"}
    except Exception as e:
        return {"status": f"❌ Error: {str(e)}", "earned": "-", "total": "-", "day": "-"}

def clear_daily_task(access_token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
        "origin": "https://airdrop.lifenetworks.io",
        "referer": "https://airdrop.lifenetworks.io/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    payload = {
        "missionId": 1,
        "answers": [
            {"questionId": i, "selectedOptionNumber": 2} for i in range(1, 6)
        ]
    }
    try:
        res = requests.post(API_TASK, headers=headers, data=json.dumps(payload))
        if res.status_code == 201:
            data = res.json().get("data", {})
            return {
                "status": "✅ Sukses",
                "earned": data.get("earnedPoints", "0"),
                "score": data.get("dailyScore", "?"),
                "message": data.get("analysisMessageEn", "")
            }
        elif res.status_code == 409:
            return {
                "status": "⏳ Sudah kerjakan daily mission",
                "earned": "0",
                "score": "-",
                "message": "Tunggu 24 jam untuk misi berikutnya"
            }
        else:
            return {"status": f"❌ Gagal ({res.status_code})", "earned": "-", "score": "-", "message": ""}
    except Exception as e:
        return {"status": f"❌ Error: {str(e)}", "earned": "-", "score": "-", "message": str(e)}

def run_once():
    print("────────────────────────────────────────────")
    print("🤖 Life Airdrop Auto Bot")
    print("🔹 Login + Check-in + Clear Daily Task")
    print("By ADFMIDN TEAM")
    print("────────────────────────────────────────────\n")

    tokens = read_tokens()
    if not tokens:
        return

    for i, t in enumerate(tokens, 1):
        id_token = t["idToken"]
        user_email = t["userEmail"]

        print(f"➡️  Akun {i}: {user_email or '(email tidak diketahui)'}")
        result = login_with_idtoken(id_token, user_email)
        time.sleep(1)

        if "error" in result:
            print(f"   ❌ Login gagal: {result['error']}\n")
            continue

        access_token = result["accessToken"]
        print(f"   ✅ Login berhasil | ID: {result['userId']} | Poin: {result['point']}")

        checkin = daily_checkin(access_token)
        print(f"   🗓️  Daily Check-in: {checkin['status']} | Earned: {checkin['earned']}")

        task = clear_daily_task(access_token)
        print(f"   🧩 Daily Mission: {task['status']} | Earned: {task['earned']} | Pesan: {task['message']}\n")

        time.sleep(1)

    print("────────────────────────────────────────────")
    print("✅ Semua akun selesai diproses!")
    print("────────────────────────────────────────────\n")

def main():
    while True:
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n🕒 Mulai proses pada: {start_time}\n")

        run_once()

        print("🕓 Menunggu 24 jam sebelum menjalankan ulang...\n")
        for i in range(24 * 60): 
            time.sleep(60)
            print(f"⏳ Sudah menunggu {i+1}/1440 menit...", end="\r")

        print("\n🔁 Memulai ulang proses...\n")


if __name__ == "__main__":
    main()
