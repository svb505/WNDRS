import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

SENDER_EMAIL = "developpersvbstd22@gmail.com"
PASSWORD = "bdhdfgkueenhdzhc"

def send_email(to, subject, html, attachments=None,app_password = PASSWORD,sender_email = SENDER_EMAIL):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(html, "html"))

        # Прикрепление файлов
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)
                else:
                    print(f"⚠️ File not found: {file_path}")

        # Отправка письма
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to, msg.as_string())
        server.quit()

        print("✅ Email sent")
    except Exception as e:
        print(f"❌ Error: {e}")
