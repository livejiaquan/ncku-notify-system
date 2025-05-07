import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time

# 動態創建檔案路徑
project_dir = os.path.dirname(os.path.abspath(__file__))  # 當前專案目錄
announcements_dir = os.path.join(project_dir, 'announcements')  # 儲存公告的資料夾
filename = os.path.join(announcements_dir, 'announcements.txt')  # 公告檔案路徑

# 確保儲存公告的資料夾存在，如果不存在則創建
if not os.path.exists(announcements_dir):
    os.makedirs(announcements_dir)

# 檢查檔案是否存在
if not os.path.exists(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        
        pass  # 建立空檔案

# 打印帶有時間戳的訊息
def print_with_time(message):
    current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
    print(current_time + message)

# 設置 headless 模式的選項
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 啟用 headless 模式
    chrome_options.add_argument("--disable-gpu")  # 避免某些系統上的 bug
    chrome_options.add_argument("--no-sandbox")  # 適用於無頭環境
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免資源使用過多
    service = Service()  # 替換為你的 chromedriver 路徑
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# 爬取網頁公告
def fetch_announcements(driver, only_today=False):
    driver.get('https://oia.ncku.edu.tw/?Lang=zh-tw')
    time.sleep(3)  # 等待網頁完全加載

    # 獲取網頁的 HTML 並解析
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 找到公告區塊
    all_announcements_section = soup.find('div', id='cmb_48_0')
    new_announcements = []
    current_date = datetime.now().strftime('%Y-%m-%d')  # 獲取當前日期

    if all_announcements_section:
        # 找到公告項目，並抓取每個公告的日期
        for announcement in all_announcements_section.find_all('div', class_='d-item d-title col-sm-12'):
            title = announcement.find('a').text.strip()
            link = announcement.find('a')['href'].strip()
            # 找到日期
            date = announcement.find('i', class_='mdate after').text.strip()

            # 如果只抓取當前日期的公告
            if only_today:
                if date == current_date:  # 如果日期為今天，才加入
                    new_announcements.append((title, link, date))
            else:
                new_announcements.append((title, link, date))

    return new_announcements

# 找出新的公告
def get_new_announcements(new_data, saved_titles):
    # 比對公告標題和日期，檢查是否已儲存
    return [(title, link, date) for title, link, date in new_data if f"{date}: {title}" not in saved_titles]

# 讀取已儲存的公告
def read_saved_titles():
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

# 儲存新的公告到檔案，將新的公告寫入最上面
def save_new_announcements(new_found):
    # 讀取目前已儲存的公告
    with open(filename, 'r', encoding='utf-8') as f:
        existing_titles = f.readlines()  # 讀取所有現有的公告

    # 打開檔案以寫入模式，並將新的公告插入最前面
    with open(filename, 'w', encoding='utf-8') as f:
        # 先將新公告寫入最前面，並標示日期
        for title, link, date in new_found:
            f.write(f"{date}: {title}\n")  # 寫入新公告

        # 然後再將舊的公告寫入
        f.writelines(existing_titles)  # 寫入舊的公告

# 主邏輯
def main():
    # 設定是否只抓取今天的公告
    only_today = False  # 將此設為 False 會抓取所有公告，True 只抓取今天的公告

    driver = setup_driver()
    new_data = fetch_announcements(driver, only_today=only_today)

    if only_today:
        # 直接顯示今天的公告，不進行儲存
        if new_data:
            message = "\n📢 成大國際事務處今天的新公告：\n\n"
            for title, link, date in new_data:
                message += f"🔹 {date} - {title}\n🔗 {link}\n\n"
            print_with_time("有新的公告！以下是詳細內容：")
            print(message)
        else:
            print_with_time("今天沒有新的公告")
    else:
        # 讀取已儲存的公告標題
        saved_titles = read_saved_titles()

        # 找出新的公告
        new_found = get_new_announcements(new_data, saved_titles)

        if new_found:
            # 構造訊息並打印
            message = "\n📢 成大國際事務處新公告：\n\n"
            for title, link, date in new_found:
                message += f"🔹 {date} - {title}\n🔗 {link}\n\n"

            # 打印結果
            print_with_time("有新的公告！以下是詳細內容：")
            print(message)

            # 如果 only_today = False，才儲存公告到檔案
            save_new_announcements(new_found)
        else:
            print_with_time("沒有新的公告")

    # 關閉瀏覽器
    driver.quit()

if __name__ == "__main__":
    main()
