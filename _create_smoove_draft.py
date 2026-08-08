#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""יוצר טיוטת קמפיין בסמוב עם גוף HTML ב-RTL וקישורי CTA מוטמעים."""
import json, urllib.request

KEY = ""
for line in open("/Users/adisomech/smoove-crm-sync/.env"):
    if line.startswith("SMOOVE_API_KEY="):
        KEY = line.strip().split("=", 1)[1]

LIST_COMMUNITY = 962460  # "רשימת תפוצה"
LINK = "https://webinar.mominvest.co.il"

cta_inline = ('<p style="text-align:center;margin:22px 0;">'
              '<a href="%s" style="color:#EF55A5;font-weight:800;font-size:18px;text-decoration:none;">%s &gt;&gt;</a></p>')
cta_button = ('<p style="text-align:center;margin:30px 0;">'
              '<a href="%s" style="background:#EF55A5;color:#191A2E;font-weight:800;font-size:18px;'
              'text-decoration:none;padding:15px 36px;border-radius:100px;display:inline-block;">%s &gt;&gt;</a></p>') % (
              LINK, "לשריון מקום בשידור החינמי")

body = """<div dir="rtl" style="max-width:600px;margin:0 auto;padding:8px 18px;font-family:'Assistant','Heebo',Arial,sans-serif;font-size:17px;line-height:1.75;color:#191A2E;text-align:right;background:#FBFAF7;">

<p>היי,</p>

<p>לפני קצת יותר משנה ישבתי מול המסך, עם עסק פעיל ועמוס, ואמרתי לעצמי משפט שאולי גם את אומרת לעצמך לפעמים:</p>

<p style="font-style:italic;color:#6B6B7B;">"יש לי מלא מה לתת. אבל אין לי מושג איך להפוך את זה למשהו אמיתי."</p>

<p>לא הייתה לי תכנית עסקית לחמש שנים. לא ידעתי את כל הצעדים מראש. מה שכן היה לי זה <strong>שליחות אחת שהרגשתי צורך אמיתי להעביר הלאה.</strong></p>

<p>אז לקחתי אותה, ובניתי מיזם פשוט שקראתי לו &rdquo;משקיעה בעצמי&rdquo;.</p>

%s

<p>ותשמעי כמה זה מטורף: אני בכלל לא העברתי את התוכן בעצמי. אני לא רואת חשבון ולא יועצת השקעות, ולא ניסיתי להעמיד פנים שאני יודעת הכל. מה שכן ידעתי לעשות זה <strong>לחבר.</strong> לקחתי אנשי מקצוע מדהימים, והבאתי אותם אל נשים אלופות שרוצות להתחיל להשקיע ופשוט לא ידעו מאיפה.</p>

<p>זו הייתה כל המתנה שלי. לא הידע. <strong>החיבור.</strong></p>

<p>והמחזור הראשון של &rdquo;משקיעה בעצמי&rdquo; הצליח הרבה מעבר למה שדמיינתי. כמעט <strong>70 אלף שקל</strong> כבר במחזור הראשון, ממשהו שחודש קודם היה רק רעיון בראש.</p>

<p style="font-size:22px;font-weight:800;line-height:1.4;color:#191A2E;">את לא צריכה להיות המומחית.<br>את צריכה את המתנה שכבר יש בך,<br>ומסגרת שתהפוך אותה למיזם שמוכר.</p>

<p>באותה שנה ראשונה, במקביל לעסק, כל זה הכניס לי <strong>מעל חצי מיליון שקל</strong> מתכניות ליווי. ומאז ליוויתי <strong>מעל 20 נשים</strong> שעשו בדיוק את אותו הדבר, כל אחת מהמתנה שלה, והכניסו כבר עשרות אלפי שקלים.</p>

<p>לא כי הן הפכו למשפיעניות. לא כי היו להן קורסים מטורפים או קהל ענק. אלא כי הן הפסיקו לחפש עוד ידע, והתחילו לזקק את מה שכבר היה בהן.</p>

%s

<p>ביום שני בערב אני עושה על זה שידור חי, פעם אחת בלבד, 100 מקומות בזום. ואני הולכת להראות לך שלושה דברים:</p>

<p>&#9989; למה עוד קורס לא באמת יזיז אותך<br>
&#9989; איך לזהות את הנכס שכבר יושב בך היום<br>
&#9989; ואיך מוכרים אותו עוד לפני שהכל מוכן, בלי להמר על שנה מהחיים</p>

<p style="font-weight:800;font-size:18px;">יום שני, 10.8, בשעה 20:30. בזום, וחינם.</p>

<p>זו לא עוד הרצאה כללית. זה בדיוק הצעד שהלוואי שמישהי הייתה נותנת לי לפני שנה.</p>

%s

<p>המקומות מוגבלים ל-100. אז אם זה מדבר אלייך, שרייני מקום עכשיו, לפני שהם ייגמרו.</p>

<p>מתרגשת לפגוש אותך שם,<br>עדי</p>

<p style="color:#6B6B7B;font-size:15px;border-top:1px solid #ECE7DF;padding-top:14px;"><strong>נ.ב.</strong> אם יש לך בן זוג, שבו לצפות ביחד. הרבה יותר קל להחליט על הצעד הבא כששניכם ראיתם את אותה תמונה.</p>

</div>""" % (
    cta_inline % (LINK, "לשריון מקום בשידור החינמי"),
    cta_inline % (LINK, "אני רוצה לשריין מקום בשידור החינמי"),
    cta_button,
)

payload = {
    "subject": "יש לך כבר נכס ששווה כסף, את פשוט עוד לא יודעת מה",
    "body": body,
    "toListsById": [LIST_COMMUNITY],
    "trackLinks": True,
}

with open("/tmp/smoove_payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
print("payload written to /tmp/smoove_payload.json")
