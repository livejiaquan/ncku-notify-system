from ncku_oia_crawler import NCKUOIACrawler
from email_sender import send_email
from utils import setup_logger
import sys

def main():
    logger = setup_logger()
    
    try:
        crawler = NCKUOIACrawler()
        
        # 爬取公告
        logger.info("開始爬取公告...")
        announcements = crawler.fetch_announcements(only_today=False)
        
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
                raise
        else:
            logger.info("沒有新的公告")

    except Exception as e:
        logger.error(f"程式執行過程中發生錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 