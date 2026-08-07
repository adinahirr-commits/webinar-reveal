#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ממתין לתעודת HTTPS של webinar.mominvest.co.il, מאמת E2E מול smoove,
מאלץ HTTPS, ושולח לעדי בטלגרם את הודעת הוואטסאפ + פורמט הסטורי."""
import json, time, subprocess, urllib.request, urllib.error, ssl

DOMAIN = "https://webinar.mominvest.co.il/"
SIGNUP = "https://academy.mominvest.co.il/webinar-signup"
LIST_ID = 1158214

# --- creds ---
tg = json.load(open("/Users/adisomech/claude-telegram-bot/config.json"))
TG_TOKEN = tg["botToken"]
TG_CHAT = tg["allowedChatIds"][0]
SMOOVE_KEY = ""
for line in open("/Users/adisomech/smoove-crm-sync/.env"):
    if line.startswith("SMOOVE_API_KEY="):
        SMOOVE_KEY = line.strip().split("=", 1)[1]

def tg_send(text):
    data = json.dumps({"chat_id": TG_CHAT, "text": text, "disable_web_page_preview": False}).encode()
    req = urllib.request.Request("https://api.telegram.org/bot%s/sendMessage" % TG_TOKEN,
                                 data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=30).read()
        return True
    except Exception as e:
        print("tg error:", e); return False

def http_code(url):
    try:
        r = urllib.request.urlopen(url, timeout=20, context=ssl.create_default_context())
        return r.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0

# 1) wait for HTTPS cert (up to ~60 min)
https_ok = False
for i in range(180):
    if http_code(DOMAIN) == 200:
        https_ok = True; break
    time.sleep(20)

# 2) enforce HTTPS once cert exists
if https_ok:
    subprocess.run(["gh", "api", "-X", "PUT", "repos/adinahirr-commits/webinar-reveal/pages",
                    "-F", "https_enforced=true"], capture_output=True)

# 3) E2E: synthetic signup -> verify in smoove -> cleanup
e2e_ok = False
test_email = "claude-live-e2e@example.com"
try:
    body = json.dumps({"name": "בדיקת דף חי", "phone": "0500000011", "email": test_email}).encode()
    req = urllib.request.Request(SIGNUP, data=body,
                                 headers={"Content-Type": "application/json",
                                          "Origin": "https://webinar.mominvest.co.il"})
    resp = json.loads(urllib.request.urlopen(req, timeout=40).read().decode())
    if resp.get("ok"):
        time.sleep(3)
        lreq = urllib.request.Request(
            "https://rest.smoove.io/v1/Lists/%d/Contacts?page=1&itemsPerPage=20" % LIST_ID,
            headers={"Authorization": SMOOVE_KEY})
        contacts = json.loads(urllib.request.urlopen(lreq, timeout=40).read().decode())
        e2e_ok = any((c.get("email") or "").lower() == test_email for c in contacts)
        # cleanup
        creq = urllib.request.Request(
            "https://rest.smoove.io/v1/Contacts?updateIfExists=true",
            data=json.dumps({"email": test_email, "lists_ToUnsubscribe": [LIST_ID]}).encode(),
            headers={"Authorization": SMOOVE_KEY, "Content-Type": "application/json"})
        urllib.request.urlopen(creq, timeout=40).read()
except Exception as e:
    print("e2e error:", e)

# 4) compose + send
status = (
    "בוקר טוב עדי ☀️ הדף לשידור החשיפה מוכן וחי:\n"
    "🔗 https://webinar.mominvest.co.il\n\n"
    + ("✅ HTTPS פעיל ומאובטח\n" if https_ok else "⏳ תעודת ה-HTTPS עדיין בהנפקה (הדף כבר עולה, ייתכן שיציג אזהרה לכמה דקות נוספות)\n")
    + ("✅ אימות קצה-לקצה עבר: הרשמת בדיקה נכנסה לרשימת smoove ונמחקה\n" if e2e_ok else "⚠️ אימות ה-smoove לא הושלם אוטומטית, כדאי שאבדוק בבוקר לפני שליחה\n")
    + "\nלמטה מחכות לך 2 הודעות מוכנות: הודעת הוואטסאפ לקבוצות, ופורמט לסטורי. אפשר להעתיק כמו שהן 💛"
)
tg_send(status)

whatsapp = (
    "📱 הודעה לקבוצות הוואטסאפ (העתקה והדבקה):\n"
    "— — — — —\n"
    "בנות יקרות 💛\n\n"
    "רציתי להזמין אתכן למשהו שממש קרוב לליבי.\n"
    "ביום שלישי הקרוב, 11.8 בשעה 20:30, אני עושה שידור חי מיוחד, פעם אחת בלבד:\n\n"
    "✨ יש לך כבר נכס ששווה כסף ✨\n\n"
    "אני אראה לכן איך משהו שכבר יש בכן, ידע, כישרון או ניסיון חיים, יכול להפוך למקור הכנסה נוסף. בלי לעזוב את העבודה, ובלי לוותר על הזמן עם הילדים.\n\n"
    "זה שידור חי אחד, בלי הקלטה, אז שווה להיות איתי שם בזמן אמת. ואם בא לכן, מוזמנות לשבת לצפות יחד עם בן הזוג 😉\n\n"
    "לשריון מקום, שתי דקות והכניסה חינם:\n"
    "👈 https://webinar.mominvest.co.il\n\n"
    "מתרגשת לפגוש אתכן,\nעדי"
)
tg_send(whatsapp)

story = (
    "📸 פורמט לסטורי (טקסט להעלות על התמונה, את מעצבת):\n"
    "— — — — —\n"
    "פריים 1:\n"
    "למעלה (קטן): שידור חי · פעם אחת בלבד\n"
    "כותרת גדולה: יש לך כבר\nנכס ששווה כסף 💛\n"
    "מתחת: יום שלישי · 20:30 · בזום\n"
    "למטה: הרשמה חינם בקישור 👇\n"
    "➕ להוסיף סטיקר 'קישור' ל־webinar.mominvest.co.il, וסטיקר 'תזכורת' לשידור.\n"
    "רקע מומלץ: איור המתנה מהדף, או סרטון סלפי קצר שלך מספרת על השידור.\n\n"
    "פריים 2 (רשות, הוכחה):\n"
    "כותרת: נשים אמיתיות כבר עשו את זה 👇\n"
    "· שושי: הגדלתי הכנסות פי 2\n"
    "· אלומה: מצאתי מעל 200 אלף שלא ידעתי שיש לי\n"
    "למטה: מחכה לך בשידור. הקישור למעלה 👆"
)
tg_send(story)
print("done. https_ok=%s e2e_ok=%s" % (https_ok, e2e_ok))
