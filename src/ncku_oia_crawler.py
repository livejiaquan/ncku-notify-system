import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import logging
from config import load_config
from utils import setup_logger

class NCKUOIACrawler:
    def __init__(self):
        self.logger = setup_logger()
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.announcements_dir = os.path.join(self.project_root, 'data', 'announcements')
        self.filename = os.path.join(self.announcements_dir, 'announcements.txt')
        self._ensure_directories()
        self.max_retries = 3
        self.retry_delay = 5  # 秒

    def _ensure_directories(self):
        """確保必要的目錄存在"""
        try:
            if not os.path.exists(self.announcements_dir):
                os.makedirs(self.announcements_dir)
            if not os.path.exists(self.filename):
                with open(self.filename, 'w', encoding='utf-8') as f:
                    pass
        except OSError as e:
            self.logger.error(f"創建目錄或文件時發生錯誤: {e}")
            raise

    def _setup_driver(self):
        """設置 Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            service = Service()
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            self.logger.error(f"設置WebDriver時發生錯誤: {e}")
            raise

    def fetch_announcements(self, only_today=False):
        """爬取公告，包含重試機制"""
        for attempt in range(self.max_retries):
            try:
                return self._fetch_announcements_impl(only_today)
            except WebDriverException as e:
                if attempt == self.max_retries - 1:
                    self.logger.error(f"爬取失敗，已達到最大重試次數: {e}")
                    raise
                self.logger.warning(f"爬取失敗，正在進行第{attempt + 1}次重試")
                time.sleep(self.retry_delay)

    def _fetch_announcements_impl(self, only_today):
        """實際的爬取邏輯"""
        driver = self._setup_driver()
        try:
            self.logger.info("開始爬取成大國際處網站")
            driver.get('https://oia.ncku.edu.tw/?Lang=zh-tw')
            time.sleep(3)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            announcements_section = soup.find('div', id='cmb_48_0')
            
            if not announcements_section:
                self.logger.warning("未找到公告區塊")
                return []

            current_date = datetime.now().strftime('%Y-%m-%d')
            announcements = []

            for item in announcements_section.find_all('div', class_='d-item d-title col-sm-12'):
                announcement = self._parse_announcement(item, current_date, only_today)
                if announcement:
                    announcements.append(announcement)

            self.logger.info(f"成功爬取到 {len(announcements)} 條公告")
            return announcements
        finally:
            driver.quit()

    def _parse_announcement(self, item, current_date, only_today):
        """解析單條公告"""
        try:
            title = item.find('a').text.strip()
            link = item.find('a')['href'].strip()
            date = item.find('i', class_='mdate after').text.strip()

            if only_today and date != current_date:
                return None

            return {
                'title': title,
                'link': link,
                'date': date
            }
        except Exception as e:
            self.logger.warning(f"解析公告時發生錯誤: {e}")
            return None

    def get_new_announcements(self, announcements):
        """檢查新公告"""
        saved_titles = self._read_saved_titles()
        return [ann for ann in announcements 
                if f"{ann['date']}: {ann['title']}" not in saved_titles]

    def _read_saved_titles(self):
        """讀取已保存的公告"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines()

    def save_announcements(self, announcements):
        """保存新公告"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            existing = f.readlines()

        with open(self.filename, 'w', encoding='utf-8') as f:
            for ann in announcements:
                f.write(f"{ann['date']}: {ann['title']}\n")
            f.writelines(existing)

    def format_email_content(self, announcements):
        """格式化郵件內容"""
        if not announcements:
            return None, None

        subject = "成大國際事務處新公告通知"
        body = "\n📢 成大國際事務處新公告：\n\n"
        
        for ann in announcements:
            body += f"🔹 {ann['date']} - {ann['title']}\n"
            body += f"🔗 {ann['link']}\n\n"

        return subject, body 