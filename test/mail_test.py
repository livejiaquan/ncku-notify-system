import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import os

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import load_config

def test_send_email(subject=None, body=None):
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

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)

if __name__ == "__main__":
    test_send_email()
