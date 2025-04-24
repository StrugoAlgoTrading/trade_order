import smtplib
from email.mime.text import MIMEText
from ..config.settings import get_settings


class Mailer:
    def __init__(self):
        self.settings = get_settings

    def send(self, subject, body):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.settings.mail_sender
        msg["To"] = self.settings.mail_receiver

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.settings.mail_sender, self.settings.mail_password)
            server.sendmail(self.settings.mail_sender, self.settings.mail_receiver, msg.as_string())
