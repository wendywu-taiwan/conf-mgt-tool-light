import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from RulesetComparer.properties.config import SMTP

class MailSender:

    def __init__(self, mail_config):
        # self.smtp = smtplib.SMTP()
        self.smtp = smtplib.SMTP_SSL()
        self.host = SMTP.get('host')
        self.port = SMTP.get('port')
        self.login_username = SMTP.get('login_username')
        self.login_password = SMTP.get('login_password')
        self.sender = mail_config.get('sender')
        self.receiver = mail_config.get('receivers')
        self.title = mail_config.get('title')
        self.content = mail_config.get('content')
        self.msg = None

        self.connect()
        self.login()

    def connect(self):
        self.smtp.connect(self.host, self.port)
        # self.smtp.connect(self.host)

    def login(self):
        try:
            self.smtp.login(self.login_username, self.login_password)
        except Exception as e:
            print(e)

    def compose_msg(self, email_title=None, email_content=None, html_content=None):
        self.msg = MIMEMultipart()
        self.msg['From'] = self.sender
        self.msg['To'] = ", ".join(self.receiver)

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
