import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.properties.mail_setting import SMTP
from RulesetComparer.utils.logger import *


class MailSender:

    def __init__(self, mail_config):
        try:
            # for google SMTP server
            # self.smtp = smtplib.SMTP_SSL()
            self.host = SMTP.get('host')
            self.port = SMTP.get('port')
            # for audatex internal server
            self.smtp = smtplib.SMTP(self.host, self.port)
            self.login_username = SMTP.get('login_username')
            self.login_password = SMTP.get('login_password')
            self.sender = mail_config.get('sender')
            self.receiver = mail_config.get('receivers')
            self.title = mail_config.get('title')
            self.content = mail_config.get('content')
            self.msg = MIMEMultipart()

            self.connect()
            # self.login()
        except Exception as e:
            raise e

    def connect(self):
        self.smtp.connect(self.host, self.port)
        # self.smtp.connect(self.host)

    def login(self):
        self.smtp.login(self.login_username, self.login_password)

    def set_receiver(self, receivers=None):
        if receivers is None or len(receivers) == 0:
            self.msg['To'] = ", ".join(self.receiver)
        else:
            self.receiver = receivers
            self.msg['To'] = ", ".join(receivers)

    def compose_msg(self, email_title=None, email_content=None, html_content=None):
        self.msg['From'] = self.sender

        if email_title is not None:
            self.msg['Subject'] = Header(email_title, 'utf-8')
        else:
            self.msg['Subject'] = Header(self.title, 'utf-8')

        if email_content is not None:
            content = MIMEText(email_content, _charset='gbk')
            self.msg.attach(content)

        if html_content is not None:
            content = MIMEText(html_content, 'html', 'utf-8')
            self.msg.attach(content)

    def add_attachment(self, full_file_name, file_name, application):
        with open(full_file_name, 'rb') as attachment:
            if application == 'text':
                attachment = MIMEText(attachment.read(), _subtype='octet-stream', _charset='utf-8')
            elif application == 'image':
                attachment = MIMEImage(attachment.read(), _subtype='octet-stream')
            elif application == 'audio':
                attachment = MIMEAudio(attachment.read(), _subtype='octet-stream')
            else:
                attachment = MIMEApplication(attachment.read(), _subtype='octet-stream')

            attachment.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file_name))
            self.msg.attach(attachment)

    def send(self):
        self.smtp.sendmail(self.sender, self.receiver, self.msg.as_string())

    def quit(self):
        self.smtp.quit()
