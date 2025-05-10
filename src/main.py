from ncku_oia_crawler import NCKUOIACrawler
from email_sender import send_email
from utils import setup_logger
import sys
import argparse
import traceback
from datetime import datetime

def main():
    # 設置命令行參數
    parser = argparse.ArgumentParser(description='NCKU OIA 公告爬蟲系統')
    parser.add_argument('--only-today', action='store_true', 
                      help='僅爬取今天的公告')
    args = parser.parse_args()
    
    logger = setup_logger()
    
    try:
        crawler = NCKUOIACrawler()
        
        # 爬取公告，使用命令行參數
        logger.info("開始爬取公告...")
        logger.info(f"只爬取今天的公告: {args.only_today}")
        announcements = crawler.fetch_announcements(only_today=args.only_today)
        
        # 檢查新公告
        new_announcements = crawler.get_new_announcements(announcements)
        
        if new_announcements:
            logger.info(f"發現 {len(new_announcements)} 條新公告")
            
            # 保存新公告
            crawler.save_announcements(new_announcements)
            
            # 準備並發送郵件
            subject, body = crawler.format_email_content(new_announcements)
            try:
                send_email(subject=subject, body=body)
                logger.info("郵件發送成功")
            except Exception as e:
                logger.error(f"發送郵件時發生錯誤: {e}")
                # 發送錯誤通知郵件
                send_error_notification("發送郵件失敗", str(e), traceback.format_exc())
                raise
        else:
            logger.info("沒有新的公告")

    except Exception as e:
        error_message = f"程式執行過程中發生錯誤: {e}"
        logger.error(error_message)
        # 發送錯誤通知郵件
        send_error_notification("爬蟲程式執行失敗", str(e), traceback.format_exc())
        sys.exit(1)

def send_error_notification(error_type, error_message, error_traceback):
    """發送錯誤通知郵件"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"[錯誤通知] NCKU OIA 爬蟲系統 - {error_type} ({current_time})"
    
    body = f"""
<html>
<body>
<h2>NCKU OIA 爬蟲系統錯誤通知</h2>
<p>時間：{current_time}</p>
<p>錯誤類型：{error_type}</p>
<p>錯誤信息：</p>
<pre>{error_message}</pre>
<p>詳細錯誤追踪：</p>
<pre>{error_traceback}</pre>
</body>
</html>
"""
    
    try:
        send_email(subject=subject, body=body, is_html=True)
        print(f"已發送錯誤通知郵件：{error_type}")
    except Exception as email_error:
        print(f"發送錯誤通知郵件時發生錯誤: {email_error}")

if __name__ == "__main__":
    main() 