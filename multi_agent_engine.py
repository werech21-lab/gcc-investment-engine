import json
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ملف لتخزين معرفات أو عناوين الفرص التي تم إرسالها مسبقاً لمنع التكرار
SENT_FILE = "sent_opportunities.json"


def load_sent_opportunities():
  """تحميل قائمة الفرص المرسلة مسبقاً من الملف"""
  if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r", encoding="utf-8") as f:
      try:
        return json.load(f)
      except json.JSONDecodeError:
        return []
  return []


def save_sent_opportunity(opp_identifier):
  """حفظ معرف الفرصة بعد إرسالها بنجاح"""
  sent_list = load_sent_opportunities()
  if opp_identifier not in sent_list:
    sent_list.append(opp_identifier)
    with open(SENT_FILE, "w", encoding="utf-8") as f:
      json.dump(sent_list, f, ensure_ascii=False, indent=4)


def send_email_alert(opportunity):
  """دالة إرسال الإيميل مع التحقق من عدم التكرار"""

  # نعتمد على عنوان الفرصة كمعيار فريد للتحقق
  opp_identifier = opportunity.get("title")

  if not opp_identifier:
    print("خطأ: الفرصة لا تحتوي على عنوان واضح.")
    return

  # التحقق مما إذا كانت الفرصة أُرسلت من قبل
  sent_list = load_sent_opportunities()
  if opp_identifier in sent_list:
    print(
        f"تخطي: الفرصة ({opp_identifier}) تم إرسالها للمستثمرين مسبقاً ولا داعي"
        " للتكرار."
    )
    return

  # جلب بيانات الاعتماد من البيئة (GitHub Secrets)
  sender_email = os.environ.get("EMAIL_USER")
  app_password = os.environ.get("EMAIL_PASS")

  # البريد المستهدف
  receiver_email = "werech21@gmail.com"

  if not sender_email or not app_password:
    print(
        "خطأ: لم يتم ضبط بيانات البريد الإلكتروني في متغيرات البيئة (Secrets)."
    )
    return

  # محتوى الرسالة
  subject = "🏛️ تقرير GCC Multi-Agent: فرصة استثمارية مؤكدة"

  html_content = f"""
    <html>
      <body dir="rtl" style="font-family: Arial, sans-serif;">
        <h2>🏛️ تقرير GCC Multi-Agent الاستثماري</h2>
        <p><b>الفرصة:</b> {opportunity.get('title')}</p>
        <p><b>السعر:</b> ${opportunity.get('price')}</p>
        <p><b>التقييم:</b> {opportunity.get('rating')}</p>
        <p><b>العائد المتوقع:</b> {opportunity.get('roi')}%</p>
        <p><b>الدولة:</b> {opportunity.get('country')}</p>
        <p><b>المصدر:</b> <a href="{opportunity.get('source_link')}">رابط المصدر الرسمي</a></p>
        <hr>
        <h3>تحليل مجلس الوكلاء:</h3>
        <p>{opportunity.get('analysis')}</p>
      </body>
    </html>
    """

  msg = MIMEMultipart("alternative")
  msg["Subject"] = Header(subject, "utf-8")
  msg["From"] = sender_email
  msg["To"] = receiver_email
  msg.attach(MIMEText(html_content, "html", "utf-8"))

  try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login(sender_email, app_password)
      server.sendmail(sender_email, receiver_email, msg.as_string())

    print(f"تم إرسال الفرصة بنجاح: {opp_identifier}")

    # حفظ الفرصة في قائمة المرسل لضمان عدم تكرارها نهائياً
    save_sent_opportunity(opp_identifier)

  except Exception as e:
    print(f"حدث خطأ أثناء إرسال البريد: {e}")


if __name__ == "__main__":
  # الفرصة الحالية (يمكنك لاحقاً ربطها بمصدر جلب البيانات الفعلي لديك)
  sample_opportunity = {
      "title": "فرصة الاستثمار في الطاقة المتجددة - مشروع الخليج",
      "price": "500,000",
      "rating": "9/10",
      "roi": "11.5",
      "country": "الإمارات",
      "source_link": (
          "https://u.ae/ar-ae/about-the-uae/strategies-and-initiatives"
      ),
      "analysis": (
          "التحليل الشامل والتحقق من المصدر للأصل: فرصة الاستثمار في الطاقة"
          " المتجددة - مشروع الخليج. التقييم المخاطري: التقييم الحالي 9/10 مع عائد"
          " متوقع 11.5%. الهيكلة التمويلية: مناسبة للاستثمار الاستراتيجي في قطاع"
          " Energy & Renewables."
      ),
  }

  send_email_alert(sample_opportunity)
