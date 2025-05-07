import os

# 動態創建檔案路徑
project_dir = os.path.dirname(os.path.abspath(__file__))  # 當前專案目錄
announcements_dir = os.path.join(project_dir, 'announcements')  # 儲存公告的資料夾
filename = os.path.join(announcements_dir, 'announcements.txt')  # 公告檔案路徑

# 確保儲存公告的資料夾存在，如果不存在則創建
if not os.path.exists(announcements_dir):
    os.makedirs(announcements_dir)

# 測試用的公告寫入，並打印檔案內容
def test_save_new_announcements(new_found):
    # 讀取目前已儲存的公告
    with open(filename, 'r', encoding='utf-8') as f:
        existing_titles = f.readlines()  # 讀取所有現有的公告

    # 打開檔案以寫入模式，並將新的公告插入最前面
    with open(filename, 'w', encoding='utf-8') as f:
        # 先將新公告寫入最前面
        for title, _ in new_found:
            f.write(title + '\n')  # 寫入新公告

        # 然後再將舊的公告寫入
        f.writelines(existing_titles)  # 寫入舊的公告

    # 打印檔案的內容來確認
    print("檔案內容：")
    with open(filename, 'r', encoding='utf-8') as f:
        print(f.read())

# 模擬新的公告
new_announcements = [
    ("【公告】國立成功大學114學年第2學期校級薦外交換學生計畫簡章", "http://example.com/1"),
    ("【公告】0328緬甸強震慰問金申請說明 Application Instructions for the 0328 Myanmar Earthquake Relief Grant", "http://example.com/2")
]

# 測試函數：插入公告並打印結果
test_save_new_announcements(new_announcements)
