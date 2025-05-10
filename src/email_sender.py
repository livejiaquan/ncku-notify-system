import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import load_config

def send_email(subject=None, body=None, is_html=False):
    # 載入配置
    config = load_config('email_config.yaml')
    
    # 從配置中獲取設置
    smtp_server = config['smtp']['server']
    smtp_port = config['smtp']['port']
    sender_email = config['email']['sender']
    sender_password = config['email']['password']
    receiver_email = config['email']['receiver']
    
    # 如果沒有提供主題和內容，使用配置中的預設值
    subject = subject or config['notification']['subject']
    body = body or config['notification']['body']

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # 根據 is_html 參數決定郵件格式
    content_type = 'html' if is_html else 'plain'
    msg.attach(MIMEText(body, content_type))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
